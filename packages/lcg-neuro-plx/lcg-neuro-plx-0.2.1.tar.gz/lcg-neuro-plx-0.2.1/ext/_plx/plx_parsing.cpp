/*
 * plx - Parsing of PLX files produced by Plexon Inc. software
 * Copyright (C) 2018  Pedro Asad
 * 
 * This program is free software: you can redistribute it and/or modify it under
 * the terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
 * details.
 * 
 * You should have received a copy of the GNU General Public License along with
 * this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * If you have any questions or suggestions regarding this software, visit
 * <http://gitlab.com/lcg/v2/plx/>.
 */

#include <sys/stat.h>

#include <algorithm>
#include <cstring>
#include <iostream>
#include <vector>

#include <_plx/plx_parsing.h>
#include <_plx/plx_file.h>

/* ================================================================================================================== */
/* Auxiliary type definitions                                                                                         */
/* ================================================================================================================== */

struct PlxFileExporter {
    const std::string &plx_path;
    const std::string &event_data_path;
    const std::string &slow_data_dir;
    const std::string &spike_data_dir;

    PlxFileExporter(
            const std::string &plx_path,
            const std::string &event_data_path,
            const std::string &slow_data_dir,
            const std::string &spike_data_dir);

    ExportedChannels operator()();

private:

    std::shared_ptr<MainHeader> plx_header;
    std::shared_ptr<DataBlockHeader> data_block_header;
    std::shared_ptr<struct stat> plx_file_info;

    std::ifstream plx_file;
    std::ofstream event_file;

    std::map<int16_t, std::ofstream> slow_data_files;
    std::map<int16_t, std::ofstream> spike_data_files;

    std::ifstream::pos_type data_section_start;
    std::ifstream::pos_type data_section_end;

    void export_event_block(
            const std::shared_ptr<DataBlockHeader> data_block_header);

    void export_slow_block(
            ExportedChannels &exported_channels,
            const std::string slow_data_dir,
            const std::shared_ptr<DataBlockHeader> data_block_header);

    void export_spike_block(
            ExportedChannels &exported_channels,
            const std::string &spike_data_dir,
            const std::shared_ptr<DataBlockHeader> data_block_header);
};

/* ================================================================================================================== */
/* Auxiliary template functions                                                                                       */
/* ================================================================================================================== */

template<class A>
std::string percent_of(const A pos, const A size) {
    std::stringstream string;
    string << std::setw(6) << std::setprecision(3) << 100.00f * pos / size << "%";
    return string.str();
}

/* ================================================================================================================== */
/* Additional function declarations                                                                                   */
/* ================================================================================================================== */

void check_io_error(
        std::ifstream &input_file,
        std::string struct_name,
        size_t bytes_to_read);

/* ================================================================================================================== */
/* Function definitions                                                                                               */
/* ================================================================================================================== */

void check_io_error(
        std::ifstream &input_file,
        std::string struct_name,
        size_t bytes_to_read) {

    if (input_file.gcount() != bytes_to_read) {
        std::cerr << std::endl
                << "ERROR: Could not read entire " << struct_name << " (" << bytes_to_read << " bytes) at position "
                << input_file.tellg() - input_file.gcount()
                << "; only " << input_file.gcount() << " bytes were read"
                << "; file could be ill-formed. Exiting..."
                << std::endl;
        exit(EXIT_FAILURE);
    } else if (input_file.fail()) {
        std::cerr << std::endl
                << "ERROR: Some irrecoverable error happened while reading a " << struct_name << ". Exiting..."
                << std::endl;
        exit(EXIT_FAILURE);
    }
}

ExportedChannels export_channels(
        const std::string &plx_path,
        const std::string &event_data_path,
        const std::string &slow_data_dir,
        const std::string &spike_data_dir) {
    return PlxFileExporter(plx_path, event_data_path, slow_data_dir, spike_data_dir)();
}

PlxFileExporter::PlxFileExporter(
    const std::string &plx_path, const std::string &event_data_path,
    const std::string &slow_data_dir, const std::string &spike_data_dir):
        plx_path(plx_path), event_data_path(event_data_path),
        slow_data_dir(slow_data_dir), spike_data_dir(spike_data_dir),
        plx_header(new MainHeader),
        data_block_header(new DataBlockHeader),
        plx_file_info(new struct stat) {
}

void PlxFileExporter::export_event_block(
        const std::shared_ptr<DataBlockHeader> data_block_header) {

    const size_t data_size =
            sizeof(int16_t)
            * data_block_header->NumberOfWordsInWaveform
            * data_block_header->NumberOfWaveforms;
    
    ExportedEventBlock exported_block = {
        data_block_header->converted_timestamp(),
        data_block_header->Channel,
        data_block_header->Unit,
    };

    event_file.write(reinterpret_cast<char*>(&exported_block), sizeof(ExportedEventBlock));

    plx_file.seekg(data_size, std::ios::cur);
}

void PlxFileExporter::export_slow_block(
        ExportedChannels &exported_channels,
        const std::string slow_data_dir,
        const std::shared_ptr<DataBlockHeader> data_block_header) {

    static std::shared_ptr<std::vector<int16_t>> data_buffer(new std::vector<int16_t>);

    const int16_t channel = data_block_header->Channel;

    const size_t data_size =
        sizeof(int16_t)
        * data_block_header->NumberOfWordsInWaveform
        * data_block_header->NumberOfWaveforms;

    data_buffer->reserve(data_size);

    if (slow_data_files.find(channel) == slow_data_files.end()) {
        std::stringstream path;
        path << slow_data_dir << "/" << channel << ".bin";
        slow_data_files[channel] = std::ofstream(path.str(), std::ios::out | std::ios::binary);
        if (not slow_data_files[channel]) {
            std::cerr << "ERROR: Could not open \"" << path.str() << "\" for writing." << std::endl;
            exit(EXIT_FAILURE);
        }
        exported_channels.slow.push_back(channel);
    }

    for (std::ofstream::pos_type i = slow_data_files[channel].tellp(); i < data_block_header->converted_timestamp() * sizeof(int16_t); i += 1) {
        slow_data_files[channel] << char(0);
    }

    plx_file.read(reinterpret_cast<char*>(data_buffer->data()), data_size);
    slow_data_files[channel].write(reinterpret_cast<char*>(data_buffer->data()), data_size);

//    plx_file.seekg(data_size, std::ios::cur);
}

void PlxFileExporter::export_spike_block(
        ExportedChannels &exported_channels,
        const std::string &spike_data_dir,
        const std::shared_ptr<DataBlockHeader> data_block_header) {

    static std::shared_ptr<std::vector<int16_t>> data_buffer(
        new std::vector<int16_t>(plx_header->NumPointsWave)
    );

    const int16_t channel = data_block_header->Channel;

    const size_t data_size =
            sizeof(int16_t)
            * data_block_header->NumberOfWordsInWaveform
            * data_block_header->NumberOfWaveforms;

    if (data_size != plx_header->NumPointsWave * sizeof(int16_t)) {
        std::cerr << "Ill-formed spike data block at offset " << plx_file.tellg() << ". Exiting..." << std::endl;
        exit(EXIT_FAILURE);
    }

    if (spike_data_files.find(channel) == spike_data_files.end()) {
        std::stringstream path;
        path << spike_data_dir << "/" << channel << ".bin";
        spike_data_files[channel] = std::ofstream(path.str(), std::ios::out | std::ios::binary);
        if (not spike_data_files[channel]) {
            std::cerr << "ERROR: Could not open \"" << path.str() << "\" for writing." << std::endl;
            exit(EXIT_FAILURE);
        }
        exported_channels.spikes.push_back(channel);
    }
    
    plx_file.read(reinterpret_cast<char*>(data_buffer->data()), data_size);
    
    const auto timestamp = data_block_header->converted_timestamp();
    spike_data_files[channel].write(reinterpret_cast<const char*>(&timestamp), sizeof(timestamp));
    spike_data_files[channel].write(reinterpret_cast<const char*>(&data_block_header->Unit), sizeof(data_block_header->Unit));
    spike_data_files[channel].write(reinterpret_cast<const char*>(data_buffer->data()), data_size);
    
    const auto spike_layout = spike_export_layout(plx_header->NumPointsWave);
    for (auto i = 0; i < spike_layout.second; i++)
        spike_data_files[channel] << char(0);
}

ExportedChannels PlxFileExporter::operator()() {

    ExportedChannels exported_channels;
    exported_channels.events = false;

    plx_file.open(plx_path, std::ios::in | std::ios::binary);
    if (not plx_file) {
        std::cerr << "ERROR: Could not open \"" << plx_path << "\" for reading." << std::endl;
        exit(EXIT_FAILURE);
    }

    event_file.open(event_data_path, std::ios::out | std::ios::binary);
    if (not event_file) {
        std::cerr << "ERROR: Could not open \"" << event_data_path << "\" for writing." << std::endl;
        exit(EXIT_FAILURE);
    }

    // Stat file, read main header, and skip counts and other header sections
    {
        stat(plx_path.c_str(), plx_file_info.get());

        plx_file.read(reinterpret_cast<char *>(plx_header.get()), sizeof(MainHeader));

        plx_file.seekg(sizeof(CountsHeader      )                               , std::ios::cur);
        plx_file.seekg(sizeof(SpikeChannelHeader) * plx_header->NumDSPChannels  , std::ios::cur);
        plx_file.seekg(sizeof(EventChannelHeader) * plx_header->NumEventChannels, std::ios::cur);
        plx_file.seekg(sizeof(SlowChannelHeader ) * plx_header->NumSlowChannels , std::ios::cur);
    }

    // Limits of data section
    data_section_start = plx_file.tellg();
    data_section_end = plx_file_info->st_size;

    // Loop through data section
    while (plx_file.good()) {
        // Attempt to read data block header and check for success
        {
            plx_file.read(reinterpret_cast<char*>(data_block_header.get()), sizeof(DataBlockHeader));
            if (plx_file.eof()) break;
            check_io_error(plx_file, "data block header", sizeof(DataBlockHeader));
        }

        switch (data_block_header->Type) {
            case DataBlockHeader::Type::CONTINUOUS:
                export_slow_block(exported_channels, slow_data_dir, data_block_header);
                break;

            case DataBlockHeader::Type::EVENT:
                export_event_block(data_block_header);
                exported_channels.events = true;
                break;

            case DataBlockHeader::Type::SPIKE:
                export_spike_block(exported_channels, spike_data_dir, data_block_header);
                break;

            default:
                std::cerr
                        << "Ill-formed data-block with type-code " << int(data_block_header->Type)
                        << "; should be one of "
                        << int(DataBlockHeader::Type::SPIKE) << ", "
                        << int(DataBlockHeader::Type::EVENT) << ", or "
                        << int(DataBlockHeader::Type::CONTINUOUS)
                        << std::endl;
                exit(EXIT_FAILURE);
        }
    }

    event_file.close();
    for (auto &slow_pair : slow_data_files) {
        for (std::ofstream::pos_type i = slow_pair.second.tellp(); i < plx_header->LastTimestamp * sizeof(int16_t); i += 1) {
            slow_pair.second << char(0);
        }
        slow_pair.second.close();
    }
    for (auto &spike_pair : spike_data_files) {
        spike_pair.second.close();
    }
    plx_file.close();

    return exported_channels;
}

std::pair<size_t, size_t> spike_export_layout(int num_points_wave) {
    const size_t used_size = sizeof(uint64_t) + sizeof(int16_t) + num_points_wave * sizeof(int16_t);
    const size_t total_size = 8 * ((used_size - 1) / 8 + 1);
    return { total_size, total_size - used_size };
}
