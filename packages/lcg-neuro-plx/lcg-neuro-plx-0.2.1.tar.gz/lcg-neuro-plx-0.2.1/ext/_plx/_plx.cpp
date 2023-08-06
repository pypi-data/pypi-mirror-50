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

#include <iostream>

#include <pybind11/pybind11.h>

#include <_plx/plx_parsing.h>
#include <_plx/plx_file.h>

namespace py = pybind11;

py::dict export_channels_interface(
        py::str plx_path,
        py::str event_data_path,
        py::str slow_data_dir,
        py::str spike_data_dir) {

    const ExportedChannels exported_channels = export_channels(
        std::string(plx_path),
        std::string(event_data_path),
        std::string(slow_data_dir),
        std::string(spike_data_dir)
    );

    py::dict exported_channels_dict;

    exported_channels_dict[py::str("events")] = py::bool_(exported_channels.events);
    exported_channels_dict[py::str("slow")] = py::list();
    exported_channels_dict[py::str("spikes")] = py::list();

    for (const auto &channel : exported_channels.slow)
        exported_channels_dict["slow"].cast<py::list>().append(py::int_(channel));
    
    for (const auto &channel : exported_channels.spikes)
        exported_channels_dict["spikes"].cast<py::list>().append(py::int_(channel));
        
    return exported_channels_dict;
}

/* ================================================================================================================== */
/* Module bindings                                                                                                    */
/* ================================================================================================================== */

PYBIND11_MODULE(_plx, mod) {
    mod.doc() = "Low-level C++ tools for parsing PLX files";

    mod.def("export_channels", &export_channels_interface,
        "Export event channel, and slow and spike waveform channel data from a *PLX* file.\n"
        "\n"
        "Parameters\n"
        "----------\n"
        "plx_path: str\n"
        "    Path to *PLX* file.\n"
        "\n"
        "event_data_path: str\n"
        "    Path to file where event channel data will be exported to.\n"
        "\n"
        "slow_data_dir: str\n"
        "    Path to directory where slow waveform channel data will be exported to.\n"
        "    Files will be named like\n"
        "\n"
        "        f'{slow_data_dir}/{channel}.bin'\n"
        "\n"
        "    for each channel. The exported format will be that of 2-byte signed\n"
        "    integer samples.\n"
        "\n"
        "spike_data_dir: str\n"
        "    Path to directory where (possibly) sorted spike waveform channel data will\n"
        "    be exported to. Files will be named like\n"
        "\n"
        "        f'{sorted_spike_data_dir}/{channel}.bin'\n"
        "\n"
        "    for each channel. The exported format will consist of the following fields:\n"
        "\n"
        "    * 'timestamp': 8-byte unsigend integer timestamp of spike-crossing time.\n"
        "    * 'unit': 1-byte unsigend integer unit identifier.\n"
        "    * 'waveform': sequence of 2-byte signed integer waveform samples. The\n"
        "      length of the sequence depends on the number of samples per waveform.\n"
        "\n"
        "    for each channel. The exported format will consist of the following fields:\n"
        "\n"
        "    * 'timestamp': 8-byte unsigend integer timestamp of spike-crossing time.\n"
        "    * 'waveform': sequence of 2-byte signed integer waveform samples. The\n"
        "      length of the sequence depends on the number of samples per waveform.\n"
        "\n"
        "Returns\n"
        "-------\n"
        "exported_channels: dict\n"
        "    A dictionary describing exported channels, in the same format as the one\n"
        "    returned by the :meth:`v2.plx.PlxFile.export_channels` method.\n"
        "\n",
        py::arg("plx_path"), py::arg("event_data_path"), py::arg("slow_data_dir"), py::arg("spike_data_dir")
    );
}
