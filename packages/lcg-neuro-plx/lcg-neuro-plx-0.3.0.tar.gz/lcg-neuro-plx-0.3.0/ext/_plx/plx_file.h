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

#ifndef PLX_H_
#define PLX_H_

#include <cstdint>

#define ENSURE_SIZE(name, size) \
    static_assert(\
        sizeof(name) == size, \
        "Size of " #name " struct should be " #size " bytes but it is not." \
        "Check your compiler's behavior regarding struct alignment and padding and amend the source code as needed." );

// TODO: Unused definitions: remove? At least the event channel defs are useful.
/*
const int PL_SingleWFType         = 1;
const int PL_StereotrodeWFType    = 2;     // reserved
const int PL_TetrodeWFType        = 3;     // reserved

const int PL_ExtEventType         = 4;
const int PL_ADDataType           = 5;
const int PL_StrobedExtChannel    = 257;
const int PL_StartExtChannel      = 258;   // delineates frames, sent for resume also
const int PL_StopExtChannel       = 259;   // delineates frames, sent for pause also
const int PL_Pause                = 260;   // not used
const int PL_Resume               = 261;   // not used

const int MAX_WF_LENGTH           = 56;
const int MAX_WF_LENGTH_LONG      = 120;

// If the server closes the connection, dll sends WM_CONNECTION_CLOSED message to hWndMain
const int WM_CONNECTION_CLOSED    = WM_USER + 401;
*/

// TODO: Unused definitions: remove?
/*
//
// PL_Event is used in PL_GetTimestampStructures(...)
//
struct PL_Event
{
    char    Type;                       // PL_SingleWFType, PL_ExtEventType or PL_ADDataType
    char    NumberOfBlocksInRecord;     // reserved   
    char    BlockNumberInRecord;        // reserved 
    unsigned char    UpperTS;           // Upper 8 bits of the 40-bit timestamp
    unsigned long    TimeStamp;         // Lower 32 bits of the 40-bit timestamp
    short   Channel;                    // Channel that this came from, or Event number
    short   Unit;                       // Unit classification, or Event strobe value
    char    DataType;                   // reserved
    char    NumberOfBlocksPerWaveform;  // reserved
    char    BlockNumberForWaveform;     // reserved
    char    NumberOfDataWords;          // number of shorts (2-byte integers) that follow this header 
}; // 16 bytes


//
// The same as PL_Event above, but with Waveform added
//
struct PL_Wave 
{
    char    Type;                       // PL_SingleWFType, PL_ExtEventType or PL_ADDataType
    char    NumberOfBlocksInRecord;     // reserved   
    char    BlockNumberInRecord;        // reserved 
    unsigned char    UpperTS;           // Upper 8 bits of the 40-bit timestamp
    unsigned long    TimeStamp;         // Lower 32 bits of the 40-bit timestamp
    short   Channel;                    // Channel that this came from, or Event number
    short   Unit;                       // Unit classification, or Event strobe value
    char    DataType;                   // reserved
    char    NumberOfBlocksPerWaveform;  // reserved
    char    BlockNumberForWaveform;     // reserved
    char    NumberOfDataWords;          // number of shorts (2-byte integers) that follow this header 
    short   WaveForm[MAX_WF_LENGTH];    // The actual waveform data
}; // size should be 128

//
// An extended version of PL_Wave for longer waveforms
//
struct PL_WaveLong 
{
    char    Type;                       // PL_SingleWFType, PL_ExtEventType or PL_ADDataType
    char    NumberOfBlocksInRecord;     // reserved   
    char    BlockNumberInRecord;        // reserved 
    unsigned char    UpperTS;           // Upper 8 bits of the 40-bit timestamp
    unsigned long    TimeStamp;         // Lower 32 bits of the 40-bit timestamp
    short   Channel;                    // Channel that this came from, or Event number
    short   Unit;                       // Unit classification, or Event strobe value
    char    DataType;                   // reserved
    char    NumberOfBlocksPerWaveform;  // reserved
    char    BlockNumberForWaveform;     // reserved
    char    NumberOfDataWords;          // number of shorts (2-byte integers) that follow this header 
    short   WaveForm[MAX_WF_LENGTH_LONG];   // The actual long waveform data
}; // size should be 256
 */

// TODO: I guess we have version 107 files in the V2 Dataset.
const int32_t LATEST_PLX_FILE_VERSION = 106;
const uint32_t PLX_MAGIC_NUMBER = 0x58454c50;

enum class OnOff : int32_t {
    OFF = 0,
    ON = 1,
};

struct MainHeader {

    enum class TrodalnessType : uint8_t {
        SINGLE = 1,
        STEREOTRODE = 2,
        TETRODE = 4,
    };

    uint32_t MagicNumber;       // = 0x58454c50;

    int32_t Version;            // Version of the data format; determines which data items are valid
    char Comment[128];          // User-supplied comment
    int32_t ADFrequency;        // Timestamp frequency in hertz
    int32_t NumDSPChannels;     // Number of DSP channel headers in the file
    int32_t NumEventChannels;   // Number of Event channel headers in the file
    int32_t NumSlowChannels;    // Number of A/D channel headers in the file
    int32_t NumPointsWave;      // Number of data points in waveform
    int32_t NumPointsPreThr;    // Number of data points before crossing the threshold

    int32_t Year;               // Time/date when the data was acquired
    int32_t Month;
    int32_t Day;
    int32_t Hour;
    int32_t Minute;
    int32_t Second;

    int32_t FastRead;           // reserved
    int32_t WaveformFreq;       // waveform sampling rate; ADFrequency above is timestamp freq
    double LastTimestamp;       // duration of the experimental session, in ticks

    // The following 6 items are only valid if Version >= 103
    TrodalnessType Trodalness;         // 1 for single, 2 for stereotrode, 4 for tetrode
    TrodalnessType DataTrodalness;     // trodalness of the data representation
    int8_t BitsPerSpikeSample;         // ADC resolution for spike waveforms in bits (usually 12)
    int8_t BitsPerSlowSample;          // ADC resolution for slow-channel data in bits (usually 12)
    uint16_t SpikeMaxMagnitudeMV;      // the zero-to-peak voltage in mV for spike waveform adc values (usually 3000)
    uint16_t SlowMaxMagnitudeMV;       // the zero-to-peak voltage in mV for slow-channel waveform adc values (usually 5000)

    // Only valid if Version >= 105
    uint16_t SpikePreAmpGain;          // usually either 1000 or 500

    // Only valid if Version >= 106
    char AcquiringSoftware[18];      // name and version of the software that originally created/acquired this data file
    char ProcessingSoftware[18];     // name and version of the software that last processed/saved this data file

    char Padding[10];                // so that this part of the header is 256 bytes
};
ENSURE_SIZE(MainHeader, 256);

struct CountsHeader {
    // Counters for the number of timestamps and waveforms in each channel and unit.
    // Note that even though there may be more than 4 units on any channel, these arrays only record the counts for the 
    // first 4 units in each channel.
    // Channel numbers are 1-based - array entry at [0] is unused

    //int32_t     TSCounts[130][5]; // number of timestamps[channel][unit]
    struct TSCounts_Type {
        int32_t data[130][5];
    } TSCounts;
    ENSURE_SIZE(TSCounts_Type, 130 * 5 * sizeof(int32_t));

    //int32_t     WFCounts[130][5]; // number of waveforms[channel][unit]
    struct WFCounts_Type {
        int32_t data[130][5];
    } WFCounts;
    ENSURE_SIZE(WFCounts_Type, 130 * 5 * sizeof(int32_t));

    // Starting at index 300, this array also records the number of samples for the
    // continuous channels.  Note that since EVCounts has only 512 entries, continuous
    // channels above channel 211 do not have sample counts.
    //int32_t     EVCounts[512];    // number of timestamps[event_number]
    struct EVCounts_Type {
        int32_t data[512];
    } EVCounts;
    ENSURE_SIZE(EVCounts_Type, 512 * sizeof(int32_t));
};
ENSURE_SIZE(CountsHeader, 7248);

struct FileHeader {
    MainHeader main;
    CountsHeader counts;
};
ENSURE_SIZE(FileHeader, 7504);

struct SpikeChannelHeader {

    enum class SortingMethod : int32_t {
        BOXES = 1,
        TEMPLATES = 2,
    };

    char        Name[32];       // Name given to the DSP channel
    char        SIGName[32];    // Name given to the corresponding SIG channel
    int32_t     Channel;        // DSP channel number, 1-based
    int32_t     WFRate;         // When MAP is doing waveform rate limiting, this is limit w/f per sec divided by 10
    int32_t     SIG;            // SIG channel associated with this DSP channel 1 - based
    int32_t     Ref;            // SIG channel used as a Reference signal, 1- based
    int32_t     Gain;           // actual gain divided by SpikePreAmpGain. For pre version 105, actual gain divided by 1000. 
    OnOff       Filter;         // 0 or 1
    int32_t     Threshold;      // Threshold for spike detection in a/d values
    SortingMethod     Method;   // Method used for sorting units, 1 - boxes, 2 - templates
    int32_t     NUnits;         // number of sorted units
    int16_t     Template[5][64];// Templates used for template sorting, in a/d values
    int32_t     Fit[5];         // Template fit
    int32_t     SortWidth;      // how many points to use in template sorting (template only)
    int16_t     Boxes[5][2][4]; // the boxes used in boxes sorting
    int32_t     SortBeg;        // beginning of the sorting window to use in template sorting (width defined by SortWidth)
    char        Comment[128];   // Version >=105
    uint8_t     SrcId;          // Version >=106, Plexus Source ID for this channel
    uint8_t     reserved;       // Version >=106
    uint16_t    ChanId;         // Version >=106, Plexus Channel ID within the Source for this channel
    char        Padding[40];
};
ENSURE_SIZE(SpikeChannelHeader, 1020);

struct EventChannelHeader {
    char        Name[32];       // name given to this event
    int32_t     Channel;        // event number, 1-based
    char        Comment[128];   // Version >=105
    uint8_t     SrcId;          // Version >=106, Plexus Source ID for this channel
    uint8_t     reserved;       // Version >=106
    uint16_t    ChanId;         // Version >=106, Plexus Channel ID within the Source for this channel
    char        Padding[128];
};
ENSURE_SIZE(EventChannelHeader, 296);

struct SlowChannelHeader {

    char        Name[32];       // name given to this channel
    int32_t     Channel;        // channel number, 0-based
    int32_t     ADFreq;         // digitization frequency
    int32_t     Gain;           // gain at the adc card
    OnOff       Enabled;        // whether this channel is enabled for taking data, 0 or 1
    int32_t     PreAmpGain;     // gain at the preamp

    // As of Version 104, this indicates the spike channel (PL_ChanHeader.Channel) of
    // a spike channel corresponding to this continuous data channel. 
    // <=0 means no associated spike channel.
    int32_t     SpikeChannel;

    char     Comment[128];  // Version >=105
    uint8_t  SrcId;         // Version >=106, Plexus Source ID for this channel
    uint8_t  reserved;      // Version >=106
    uint16_t ChanId;        // Version >=106, Plexus Channel ID within the Source for this channel
    char     Padding[108];
};
ENSURE_SIZE(SlowChannelHeader, 296);

struct DataBlockHeader {
    enum class Type : int16_t {
        SPIKE = 1,
        EVENT = 4,
        CONTINUOUS = 5,
    };

    Type      Type;                       // Data type; 1=spike, 4=Event, 5=continuous
    uint16_t  TimestampUpper;             // Upper 8 bits of the 40 bit timestamp
    uint32_t  TimestampLower;             // Lower 32 bits of the 40 bit timestamp
    int16_t   Channel;                    // Channel number
    int16_t   Unit;                       // Sorted unit number; 0=unsorted
    int16_t   NumberOfWaveforms;          // Number of waveforms in the data to folow, usually 0 or 1
    int16_t   NumberOfWordsInWaveform;    // Number of samples per waveform in the data to follow

    inline uint64_t converted_timestamp() const {
        return uint64_t(TimestampUpper) << 32 | uint64_t(TimestampLower);
    }
};
ENSURE_SIZE(DataBlockHeader, 16);

#endif
