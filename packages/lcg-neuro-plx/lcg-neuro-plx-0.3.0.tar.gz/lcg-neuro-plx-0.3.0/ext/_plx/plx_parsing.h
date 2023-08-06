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

#include <iomanip>
#include <fstream>
#include <map>
#include <memory>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

#include <_plx/plx_file.h>

struct ExportedEventBlock {
    uint64_t Timestamp;
    int16_t Channel;
    int16_t Unit;
    char padding[4];
};
ENSURE_SIZE(ExportedEventBlock, 16);

struct ExportedChannels {
    bool events;
    std::vector<int16_t> slow;
    std::vector<int16_t> spikes;
};

ExportedChannels export_channels(
        const std::string &plx_path,
        const std::string &event_data_path,
        const std::string &slow_data_dir,
        const std::string &spike_data_dir);

std::pair<size_t, size_t> spike_export_layout(int num_points_wave);
