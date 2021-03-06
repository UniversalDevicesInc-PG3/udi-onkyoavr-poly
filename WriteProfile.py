#!/usr/bin/env python3
import os
import io

# Create dynamic NLS and editor files with the mapping between service ID and  names.

def writeNlsSelEntries( nls_file, entry_list, nlsPrefix, logger ):
    """
    Writes the select lock in the NLS file based on what the 
    AVR has in it.  Also adds an NA and Unknown entry at the end
    so we can use this on the UI
    """
    index = 0
    for serviceName in entry_list:
        entry = nlsPrefix + str(index) + " = "+ serviceName.strip() + "\n"
        nls_file.write(entry)
        index = index + 1
    # Add the desired error related entries
    entry = nlsPrefix + str(index) + " = N/A\n"
    nls_file.write(entry)
    index = index + 1
    entry = nlsPrefix + str(index) + " = UNKNOWN\n"
    nls_file.write(entry)

def write_nls(logger, avr):
    """
    Creates the (en_us.txt) nls file using the infomration from the AVR
    to set the values and names for the lists the AVR provides
    Does so based on an index, not the  name, because the ISY 
    stores things based on the index, and if the user changes
    the name in the AVR we still want the function to work
    """
    logger.info("Writing profile/nls/en_us.txt")
    if not os.path.exists("profile/nls"):
        try:
            os.makedirs("profile/nls")
        except:
            logger.error('unable to create node NLS directory.')
    try:
        nls = open("profile/nls/en_us.txt", "w")

    #region - static code
        # Write out the standard node, command, and status entries

        nls.write("# Controller\n")
        nls.write("ND-AVRServer-NAME = Onkyo/Panasonic Nodeserver\n")
        nls.write("ND-AVRServer-ICON = GenericCtl\n")
        nls.write("ST-AVRServer-ST-NAME = Connected\n")
        nls.write("\n")

        nls.write("# Node\n")
        nls.write("ND-AVRNode-NAME = Receiver\n")
        nls.write("ND-AVRNode-ICON = GenericCtl\n")
        nls.write("\n")

        nls.write("# Status\n")
        nls.write("ST-ST-NAME = Power On\n")
        nls.write("ST-GV1-NAME  = Master Volume Level\n")
        nls.write("ST-GV2-NAME  = Input Selector\n")
        nls.write("ST-GV3-NAME  = Mute\n")
        nls.write("ST-GV4-NAME  = Listening Mode\n")
        nls.write("ST-GV5-NAME  = Late Night Mode\n")
        nls.write("ST-GV6-NAME  = AM Tuner Freq\n")
        nls.write("ST-GV7-NAME  = FM Tuner Freq\n")
        nls.write("ST-GV8-NAME  = Tuner Preset\n")
        nls.write("ST-GV9-NAME  = Tuner Temp\n")
        nls.write("ST-GV10-NAME  = Message\n")
        nls.write("ST-GV11-NAME  = Net/USB Service\n")
        nls.write("ST-GV12-NAME  = Net/USB Play Mode\n")
        nls.write("ST-GV13-NAME  = Net/USB Repeat\n")
        nls.write("ST-GV14-NAME  = Net/USB Shuffle\n")
        nls.write("ST-GV15-NAME  = Tuner Freq\n")
        nls.write("\n")

        nls.write("# Commands\n")
        nls.write("CMD-QUERY-NAME = Find Devices\n")
        nls.write("CMD-DON-NAME = On\n")
        nls.write("CMD-DOF-NAME = Off\n")
        nls.write("CMD-BRT-NAME = Vol Up\n")
        nls.write("CMD-DIM-NAME = Vol Down\n")
        nls.write("CMD-TUN_U-NAME = Tuner Up\n")
        nls.write("CMD-TUN_D-NAME = Tuner Down\n")
        nls.write("CMD-PRS_U-NAME = Preset Up\n")
        nls.write("CMD-PRS_D-NAME = Preset Down\n")
        nls.write("CMD-AMT_ON-NAME = Mute On\n")
        nls.write("CMD-AMT_OFF-NAME = Mute Off\n")
        nls.write("CMD-MVL-NAME = Set Master Volume\n")
        nls.write("CMD-SLI-NAME = Set Input\n")
        #nls.write("CMD-SLZ-NAME = Set Zone 2 Selector\n")
        nls.write("CMD-LMD-NAME = Set Listening Mode\n")
        nls.write("CMD-LTN-NAME = Set Late Night Mode\n")
        nls.write("CMD-TUNA-NAME = Set AM Freq\n")
        nls.write("CMD-TUNF-NAME = Set FM Freq\n")
        nls.write("CMD-NSV-NAME = Net/USB Service\n")
        nls.write("CMD-TUNC-NAME = Net/USB Commands\n")
        nls.write("CMD-PRS-NAME = Go to Preset\n")
        nls.write("CMD-OSD-NAME = Do OSD Action\n")
        nls.write("CMD-UPDATE-NAME = Update\n")
        nls.write("\n")

        nls.write("# Command Parameters\n")
        nls.write("CMDP-AVR_BOOL-ST-NAME = Power\n")
        nls.write("CMDP-AVR_BRT-BRT-NAME = Vol Up\n")
        nls.write("CMDP-AVR_DIM-DIM-NAME = Vol Down\n")
        nls.write("CMDP-AVR_MVL-MVL_V-NAME = Master Volume Level\n")
        nls.write("CMDP-AVR_SLI-SLI_V-NAME = Input Selector\n")
        #nls.write("CMDP-AVR_SLI-SLZ_V-NAME = Zone 2 Selector\n")
        nls.write("CMDP-AVR_LMD-LMD_V-NAME = Listening Mode\n")
        nls.write("CMDP-AVR_LTN-LTN_V-NAME = Late Night Mode\n")
        nls.write("CMDP-AVR_AM-TUN_A-NAME  = AM Frequency\n")
        nls.write("CMDP-AVR_FM-TUN_F-NAME = FM Frequency\n")
        nls.write("CMDP-AVR_NSV-TUN_N-NAME = Net/USB Service\n")
        nls.write("CMDP-AVR_NTC-TUN_C-NAME = Command Key\n")
        nls.write("CMDP-AVR_PRS-PRS_N-NAME = Preset\n")
        nls.write("CMDP-AVR_OSD-OSD_V-NAME = On-Screen Display Action\n")
        nls.write("\n")

        nls.write("# Command Formats\n")
        nls.write("PGM-CMD-MVL-FMT = /MVL_V// Vol: ${v}/\n")
        nls.write("PGM-CMD-SLI-FMT = /SLI_V// Selector: ${v}/\n")
        nls.write("PGM-CMD-TUNA-FMT = /TUN_A// AM Freq: ${v}/\n")
        nls.write("PGM-CMD-TUNF-FMT = /TUN_F// FM Freq: ${v}/\n")
        nls.write("PGM-CMD-TUNC-FMT = /TUN_C// Command: ${v}/\n")
        nls.write("PGM-CMD-NSV-FMT = /TUN_N// Service: ${v}/\n")
        nls.write("PGM-CMD-LMD-FMT = /LMD_V// Mode: ${v}/\n")
        nls.write("PGM-CMD-LTN-FMT = /LTN_V// Mode: ${v}/\n")
        nls.write("PGM-CMD-PRS-FMT = /PRS_N// Preset: ${v}/\n")
        nls.write("PGM-CMD-OSD-FMT = /OSD_V// Key: ${v}/\n")
        nls.write("\n")

        nls.write("# Select Lists\n")
        nls.write("ONOFF_SEL-0 = Off\n")
        nls.write("ONOFF_SEL-1 = On\n")
        nls.write("ONOFF_SEL-2 = Unknown\n")
        nls.write("\n")

        nls.write("YESNO_SEL-0 = No\n")
        nls.write("YESNO_SEL-1 = Yes\n")
        nls.write("YESNO_SEL-2 = Unknown\n")
        nls.write("\n")

        nls.write("# Listening Mode\n")
        nls.write("LMD_SEL-0 = STEREO\n")
        nls.write("LMD_SEL-1 = DIRECT\n")
        nls.write("LMD_SEL-2 = SURROUND\n")
        nls.write("LMD_SEL-3 = FILM/GAME-RPG\n")
        nls.write("LMD_SEL-4 = THX\n")
        nls.write("LMD_SEL-5 = ACTION/GAME-ACTION\n")
        nls.write("LMD_SEL-6 = MUSICAL/GAME-ROCK\n")
        nls.write("LMD_SEL-7 = MONO-MOVIE\n")
        nls.write("LMD_SEL-8 = ORCHESTRA\n")
        nls.write("LMD_SEL-9 = UNPLUGGED\n")
        nls.write("LMD_SEL-10 = STUDIO-MIX\n")
        nls.write("LMD_SEL-11 = TV-LOGIC\n")
        nls.write("LMD_SEL-12 = ALL-CH-STEREO\n")
        nls.write("LMD_SEL-13 = THEATER-DIMENSIONAL\n")
        nls.write("LMD_SEL-14 = ENHANCED-7/ENHANCE/GAME-SPORTS\n")
        nls.write("LMD_SEL-15 = MONO\n")
        nls.write("LMD_SEL-16 = PURE-AUDIO\n")
        nls.write("LMD_SEL-17 = MULTIPLEX\n")
        nls.write("LMD_SEL-18 = FULL-MONO\n")
        nls.write("LMD_SEL-19 = DOLBY-VIRTUAL/SURROUND-ENHANCER\n")
        nls.write("LMD_SEL-20 = DTS-SURROUND-SENSATION\n")
        nls.write("LMD_SEL-21 = AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-22 = WHOLE-HOUSE\n")
        nls.write("LMD_SEL-23 = STAGE\n")
        nls.write("LMD_SEL-24 = ACTION\n")
        nls.write("LMD_SEL-25 = MUSIC\n")
        nls.write("LMD_SEL-26 = SPORTS\n")
        nls.write("LMD_SEL-27 = STRAIGHT-DECODE\n")
        nls.write("LMD_SEL-28 = DOLBY-EX\n")
        nls.write("LMD_SEL-29 = THX-CINEMA\n")
        nls.write("LMD_SEL-30 = THX-SURROUND-EX\n")
        nls.write("LMD_SEL-31 = THX-MUSIC\n")
        nls.write("LMD_SEL-32 = THX-GAMES\n")
        nls.write("LMD_SEL-33 = THX-U2/S2/I/S-CINEMA/CINEMA2\n")
        nls.write("LMD_SEL-34 = THX-MUSICMODE/THX-U2/S2/I/S-MUSIC\n")
        nls.write("LMD_SEL-35 = THX-GAMES/THX-U2/S2/I/S-GAMES\n")
        nls.write("LMD_SEL-36 = PLII/PLIIX-MOVIE/DOLBY-ATMOS/DOLBY-SURROUND\n")
        nls.write("LMD_SEL-37 = PLII/PLIIX-MUSIC\n")
        nls.write("LMD_SEL-38 = NEO-6-CINEMA/NEO-X-CINEMA/DTS-X/NEURAL-X\n")
        nls.write("LMD_SEL-39 = NEO-6-MUSIC/NEO-X-MUSIC\n")
        nls.write("LMD_SEL-40 = PLII/PLIIX-THX-CINEMA/DOLBY-SURROUND-THX-CINEMA\n")
        nls.write("LMD_SEL-41 = NEO-6/NEO-X-THX-CINEMA/DTS-NEURAL-X-THX-CINEMA\n")
        nls.write("LMD_SEL-42 = PLII/PLIIX-GAME\n")
        nls.write("LMD_SEL-43 = NEURAL-SURR\n")
        nls.write("LMD_SEL-44 = NEURAL-THX/NEURAL-SURROUND\n")
        nls.write("LMD_SEL-45 = PLII/PLIIX-THX-GAMES/DOLBY-SURROUND-THX-GAMES\n")
        nls.write("LMD_SEL-46 = NEO-6/NEO-X-THX-GAMES/DTS-NEURAL-X-THX-GAMES\n")
        nls.write("LMD_SEL-47 = PLII/PLIIX-THX-MUSIC/DOLBY-SURROUND-THX-MUSIC\n")
        nls.write("LMD_SEL-48 = NEO-6/NEO-X-THX-MUSIC/DTS-NEURAL-X-THX-MUSIC\n")
        nls.write("LMD_SEL-49 = NEURAL-THX-CINEMA\n")
        nls.write("LMD_SEL-50 = NEURAL-THX-MUSIC\n")
        nls.write("LMD_SEL-51 = NEURAL-THX-GAMES\n")
        nls.write("LMD_SEL-52 = PLIIZ-HEIGHT\n")
        nls.write("LMD_SEL-53 = NEO-6-CINEMA-DTS-SURROUND-SENSATION\n")
        nls.write("LMD_SEL-54 = NEO-6-MUSIC-DTS-SURROUND-SENSATION\n")
        nls.write("LMD_SEL-55 = NEURAL-DIGITAL-MUSIC\n")
        nls.write("LMD_SEL-56 = PLIIZ-HEIGHT-THX-CINEMA\n")
        nls.write("LMD_SEL-57 = PLIIZ-HEIGHT-THX-MUSIC\n")
        nls.write("LMD_SEL-58 = PLIIZ-HEIGHT-THX-GAMES\n")
        nls.write("LMD_SEL-59 = PLIIZ-HEIGHT-THX-U2/S2-CINEMA\n")
        nls.write("LMD_SEL-60 = PLIIZ-HEIGHT-THX-U2/S2-MUSIC\n")
        nls.write("LMD_SEL-61 = PLIIZ-HEIGHT-THX-U2/S2-GAMES\n")
        nls.write("LMD_SEL-62 = NEO-X-GAME\n")
        nls.write("LMD_SEL-63 = PLIIX/PLII-MOVIE-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-64 = PLIIX/PLII-MUSIC-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-65 = PLIIX/PLII-GAME-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-66 = NEO-6-CINEMA-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-67 = NEO-6-MUSIC-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-68 = NEURAL-SURROUND-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-69 = NEURAL-DIGITAL-MUSIC-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-70 = DOLBY-EX-AUDYSSEY-DSX\n")
        nls.write("LMD_SEL-71 = AUTO-SURROUND\n")
        nls.write("LMD_SEL-72 = N/A\n")
        nls.write("LMD_SEL-73 = UNKNOWN\n")
        nls.write("\n")

        nls.write("#Late Night Command \n")
        nls.write("LTN_SEL-0 = OFF\n")
        nls.write("LTN_SEL-1 = LOW-DOLBYDIGITAL/ON-DOLBY-TRUEHD\n")
        nls.write("LTN_SEL-2 = HIGH-DOLBYDIGITAL\n")
        nls.write("LTN_SEL-3 = AUTO-DOLBY-TRUEHD\n")
        nls.write("LTN_SEL-4 = UP\n")
        nls.write("LTN_SEL-5 = N/A\n")
        nls.write("LTN_SEL-6 = UNKNOWN\n")
        nls.write("\n")

        nls.write("#OSD Commands\n")
        nls.write("OSD_SEL-0 = Menu\n")
        nls.write("OSD_SEL-1 = Up\n")
        nls.write("OSD_SEL-2 = Down\n")
        nls.write("OSD_SEL-3 = Right\n")
        nls.write("OSD_SEL-4 = Left\n")
        nls.write("OSD_SEL-5 = Enter\n")
        nls.write("OSD_SEL-6 = Exit\n")
        nls.write("OSD_SEL-6 = AUDIO\n")
        nls.write("OSD_SEL-7 = VIDEO\n")
        nls.write("OSD_SEL-8 = HOME\n")
        nls.write("OSD_SEL-9 = QUICK\n")
        nls.write("OSD_SEL-10 = IPV\n")
        nls.write("OSD_SEL-11 = N/A\n")
        nls.write("OSD_SEL-12 = UNKNOWN\n")
        nls.write("\n")

        nls.write("#PWR Commands\n")
        nls.write("PWR_SEL-0 = STANDBY/OFF\n")
        nls.write("PWR_SEL-1 = ON\n")
        nls.write("PWR_SEL-2 = STANDBY-ALL\n")
        nls.write("PWR_SEL-3 = N/A-Not Supported\n")
        nls.write("PWR_SEL-4 = UNKNOWN\n")
        nls.write("\n")
        nls.write("\n")

        nls.write("#Messages Commands\n")
        nls.write("MSG_SEL-0 = \n")
        nls.write("MSG_SEL-1 = Device Offline\n")
        nls.write("MSG_SEL-2 = Device returned N/A, selection not supported or not set\n")
        nls.write("MSG_SEL-3 = Error on command, check node log for details\n")
        nls.write("MSG_SEL-4 = Value error on command\n")
        nls.write("MSG_SEL-5 = Service not supported\n")
        nls.write("\n")
        nls.write("\n")
        nls.write("#Mute\n")
        nls.write("AMT_SEL-0 = OFF\n")
        nls.write("AMT_SEL-1 = ON\n")
        nls.write("AMT_SEL-2 = TOGGLE\n")
        nls.write("AMT_SEL-3 = N/A\n")
        nls.write("AMT_SEL-4 = UNKNOWN\n")
        nls.write("\n")


        nls.write("#Net Status\n")
        nls.write("NST_PLAY_SEL-0 = Stopped\n")
        nls.write("NST_PLAY_SEL-1 = Playing\n")
        nls.write("NST_PLAY_SEL-2 = Paused\n")
        nls.write("NST_PLAY_SEL-3 = FF\n")
        nls.write("NST_PLAY_SEL-4 = FR\n")
        nls.write("NST_PLAY_SEL-5 = EOF\n")
        nls.write("NST_PLAY_SEL-6 = --\n")
        nls.write("NST_PLAY_SEL-7 = Unknown\n")
        nls.write("\n")
        nls.write("NST_REPEAT_SEL-0 = Off\n")
        nls.write("NST_REPEAT_SEL-1 = All \n")
        nls.write("NST_REPEAT_SEL-2 = Folder\n")
        nls.write("NST_REPEAT_SEL-3 = Repeat Once\n")
        nls.write("NST_REPEAT_SEL-4 = Disabled\n")
        nls.write("NST_REPEAT_SEL-5 = --\n")
        nls.write("NST_REPEAT_SEL-6 = UNKNOWN\n")
        nls.write("\n")
        nls.write("NST_SHUFFLE_SEL-0 = Off \n")
        nls.write("NST_SHUFFLE_SEL-1 = All  \n")
        nls.write("NST_SHUFFLE_SEL-2 = Album \n")
        nls.write("NST_SHUFFLE_SEL-3 = Folder \n")
        nls.write("NST_SHUFFLE_SEL-4 = Disabled\n")
        nls.write("NST_SHUFFLE_SEL-5 = --\n")
        nls.write("NST_SHUFFLE_SEL-6 = UNKNOWN\n")
        nls.write("\n")

        nls.write("#Network Control\n")
        nls.write("NTC_SEL-0 = PLAY KEY\n")
        nls.write("NTC_SEL-1 = STOP KEY\n")
        nls.write("NTC_SEL-2 = PAUSE KEY\n")
        nls.write("NTC_SEL-3 = PLAY/PAUSE KEY\n")
        nls.write("NTC_SEL-4 = TRACK UP KEY\n")
        nls.write("NTC_SEL-5 = TRACK DOWN KEY\n")
        nls.write("NTC_SEL-6 = REPEAT KEY\n")
        nls.write("NTC_SEL-7 = RANDOM KEY\n")
        nls.write("NTC_SEL-8 = REPEAT/SHUFFLE KEY\n")
        nls.write("NTC_SEL-9 = DISPLAY KEY\n")
        nls.write("NTC_SEL-10 = RIGHT KEY\n")
        nls.write("NTC_SEL-11 = LEFT KEY\n")
        nls.write("NTC_SEL-12 = UP KEY\n")
        nls.write("NTC_SEL-13 = DOWN KEY\n")
        nls.write("NTC_SEL-14 = SELECT KEY\n")
        nls.write("NTC_SEL-15 = 0 KEY\n")
        nls.write("NTC_SEL-16 = 1 KEY\n")
        nls.write("NTC_SEL-17 = 2 KEY\n")
        nls.write("NTC_SEL-18 = 3 KEY\n")
        nls.write("NTC_SEL-19 = 4 KEY\n")
        nls.write("NTC_SEL-20 = 5 KEY\n")
        nls.write("NTC_SEL-21 = 6 KEY\n")
        nls.write("NTC_SEL-22 = 7 KEY\n")
        nls.write("NTC_SEL-23 = 8 KEY\n")
        nls.write("NTC_SEL-24 = 9 KEY\n")
        nls.write("NTC_SEL-25 = DELETE KEY\n")
        nls.write("NTC_SEL-26 = CAPS KEY\n")
        nls.write("NTC_SEL-27 = RETURN KEY\n")
        nls.write("NTC_SEL-28 = CH UP(for iRadio)\n")
        nls.write("NTC_SEL-29 = CH DOWN(for iRadio)\n")
        nls.write("NTC_SEL-30 = MENU\n")
        nls.write("NTC_SEL-31 = TOP MENU\n")
        nls.write("NTC_SEL-32 = MODE(for iPod) STD<->EXT\n")
        nls.write("NTC_SEL-33 = LIST <-> PLAYBACK\n")
        nls.write("NTC_SEL-34 = MEMORY (add Favorite)\n")
        nls.write("NTC_SEL-35 = Positive Feed or Mark/Unmark *1\n")
        nls.write("NTC_SEL-36 = Negative Feed *1\n")
        nls.write("NTC_SEL-37 = N/A\n")
        nls.write("NTC_SEL-38 = UNKNOWN\n")
        nls.write("\n")

        nls.write("STATUS-0 = Disconnected\n")
        nls.write("STATUS-1 = Connected\n")
        nls.write("STATUS-2 = Failed\n")
        nls.write("\n")
        #endregion  - Static code
        # Now write dynamic entires
        nls.write("#Network Services\n")
        entry_list = avr.networkServiceNamesSortedById()
        writeNlsSelEntries( nls ,entry_list, "NSV_SEL-", logger )
        nls.write('\n')

        nls.write("#Input Selectors\n")
        entry_list = avr.selectorSortedById()
        writeNlsSelEntries( nls ,entry_list, "SLI_SEL-", logger )
        nls.write('\n')
    except Exception as e:
        logger.error('Failed to write node NLS file: {}'.format(e))
    finally:
        nls.close()
    logger.info("Finsihed writing nls file")

def write_editors(logger, avr):
    """
    Creates the editors.xml file using the infomration from the AVR
    to set the values and names for the lists the AVR provides
    Uses the counts of the dynamic lists to sets ranges and the tuner
    specs to set frequency ranges
    """
    logger.info("Writing profile/editor/editors.xml")
    if not os.path.exists("profile/editor"):
        try:
            os.makedirs("profile/editor")
        except:
            logger.error('unable to create node editor directory.')
    try:
    #region - static code
        editors = open("profile/editor/editors.xml", "w")
        editors.write('<editors>\n')
        editors.write('    <!-- Status   -->\n')
        editors.write('    <editor id="STATUS">\n')
        editors.write('        <range uom="25" subset="0-2" nls="STATUS" />\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Boolean   -->\n')
        editors.write('    <editor id="AVR_BOOL">\n')
        editors.write('        <range uom="2" subset="0-1" />\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Master Volume Level -->\n')
        editors.write('    <editor id="AVR_MVL">\n')
        editors.write('        <range uom="100" min="0" max="255" prec="0" step="1" />\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Listening Mode -->\n')
        editors.write('    <editor id="AVR_LMD">\n')
        editors.write('        <range uom="25" subset= "0-79" nls = "LMD_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Late Night Mode -->\n')
        editors.write('    <editor id="AVR_LTN">\n')
        editors.write('        <range uom="25" subset= "0-3" nls = "LTN_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Temperature -->\n')
        editors.write('    <editor id="AVR_TPD">\n')
        editors.write('        <range uom="17" min="0" max="255" prec="1" step="1" />\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- On Screen Display -->\n')
        editors.write('    <editor id="AVR_OSD">\n')
        editors.write('        <range uom="25" subset= "0-10" nls = "OSD_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Network List Tracks (Services) -->\n')
        editors.write('    <editor id="AVR_NLT">\n')
        editors.write('        <range uom="25" subset= "0-26" nls = "NLT_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Net Status - Play -->\n')
        editors.write('    <editor id="AVR_NST_PLAY">\n')
        editors.write('        <range uom="25" subset= "0-7" nls = "NST_PLAY_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Net Status - Play -->\n')
        editors.write('    <editor id="AVR_NST_REPEAT">\n')
        editors.write('        <range uom="25" subset= "0-6" nls = "NST_REPEAT_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Net Status - Shuffle -->\n')
        editors.write('    <editor id="AVR_NST_SHUFFLE">\n')
        editors.write('        <range uom="25" subset= "0-6" nls = "NST_SHUFFLE_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Network Control -->\n')
        editors.write('    <editor id="AVR_NTC">\n')
        editors.write('        <range uom="25" subset= "0-36" nls = "NTC_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Power -->\n')
        editors.write('    <editor id="AVR_PWR">\n')
        editors.write('        <range uom="25" subset= "0-4" nls = "PWR_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Mute -->\n')
        editors.write('    <editor id="AVR_AMT">\n')
        editors.write('        <range uom="25" subset= "0-4" nls = "AMT_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <editor id="AVR_ONOFF">\n')
        editors.write('        <range uom="25" subset= "0-2" nls = "ONOFF_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <editor id="AVR_YESNO">\n')
        editors.write('        <range uom="25" subset= "0-2" nls = "YESNO_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('    <!-- Messages -->\n')
        editors.write('    <editor id="AVR_MSG">\n')
        editors.write('        <range uom="25" subset= "0-3" nls = "MSG_SEL"/>\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        #endregion - static code

        count= 0
        try:
            count=avr.selectorCount() # Do not add the two we add because don't want those in the UI, but do want them programatically
        except Exception as e:
            logger.info('Did not get selector count, using defaults for WriteProfile: {}'.format(e))
            count= 0
        editors.write('    <!-- Input Selector -->\n')
        editors.write('    <editor id="AVR_SLI">\n')
        editors.write('        <range uom="25" subset= "0-' + str(count) + '" nls = "SLI_SEL"/>\n') 
        editors.write('    </editor>\n')
        editors.write('\n')
        
        try:
            count=avr.presetCount()
        except Exception as e:
            logger.info('Did not get preset count, using default for WriteProfile: {}'.format(e))
            count= 0
        editors.write('    <!-- Preset -->\n')
        editors.write('    <editor id="AVR_PRS">\n')
        editors.write('        <range uom="56" min="0" max="' + str(count) + '" prec="0" step="1" />\n')  
        editors.write('    </editor>\n')
        editors.write('\n')

        try:
            count=avr.networkServicesCount() # Do not add the two we add because don't want those in the UI, but do want them programatically
        except Exception as e:
            logger.info('Did not get network services count, using defaults for WriteProfile: {}'.format(e))
            count= 0
        editors.write('    <!-- Network (Services) -->\n')
        editors.write('    <editor id="AVR_NSV">\n')
        editors.write('        <range uom="25" subset= "0-' + str(count) + '" nls = "NSV_SEL"/>\n') 
        editors.write('    </editor>\n')
        editors.write('\n')

        hasAM = False
        hasFM = False
        minFreq = '0'
        maxFreq = '0'
        amMinFreq = '0'
        amMaxFreq = '0'
        amStep = '0'
        fmMinFreq = '0'
        fmMaxFreq = '0'
        fmStep = '0'
        try:
            tuners = avr.tuners
            hasAM =  'AM' in tuners
            amMinFreq = tuners['AM']['min']
            amMaxFreq = tuners['AM']['max']
            amStep    = tuners['AM']['step']

            hasFM =  'FM' in tuners
            fmMinFreq = str(float(tuners['FM']['min'])/1000)
            fmMaxFreq = str(float(tuners['FM']['max'])/1000)
            fmStep    = str(float(tuners['FM']['step'])/1000)
        except Exception as e:
            logger.info('Did not get tuner information, using defaults for WriteProfile: {}'.format(e))
            hasAM =  True
            hasFM =  True
            amMinFreq = '530'
            amMaxFreq = '1710'
            amStep = '10'
            fmMinFreq = '87.5'
            fmMaxFreq = '107.9'
            fmStep = '0.2'

        if hasAM:
            editors.write('    <!-- AM Tuner -->\n') 
            editors.write('    <editor id="AVR_AM">\n')
            editors.write('        <range uom="56" min="'+ amMinFreq +'" max="'+ amMaxFreq +'" prec="0" step="'+ amStep +'" />\n')
            editors.write('    </editor>\n')
            editors.write('\n')
            minFreq = amMinFreq
            maxFreq = amMaxFreq
        if hasFM:
            editors.write('    <!-- FM Tuner -->\n') 
            editors.write('    <editor id="AVR_FM">\n')
            editors.write('        <range uom="56" min="'+ fmMinFreq +'" max="'+ fmMaxFreq +'" prec="1" step="'+ fmStep +'" />\n')
            editors.write('    </editor>\n')
            editors.write('\n')
            minFreq = fmMinFreq
            if maxFreq == '0':
                maxFreq = fmMaxFreq
        editors.write('    <editor id="AVR_FREQ">\n')
        editors.write('        <range uom="56" min="'+ minFreq +'" max="'+ maxFreq +'" prec="1" step="1" />\n')
        editors.write('    </editor>\n')
        editors.write('\n')
        editors.write('</editors>\n')
    except Exception as e:
        logger.error('Failed to write node editor file: {}'.format(e))
    finally: 
        editors.close()
    logger.info("Finished writing editors file")
