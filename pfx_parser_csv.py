
                if detail_soup.find("stadium"):
                    park_id = detail_soup.stadium["id"]
                    park_name = detail_soup.stadium["name"]
                    park_loc = detail_soup.stadium["location"]
                else:
                    if BeautifulSoup(urlopen(g_url), features="lxml").find("a", href="gameday_Syn.xml"):
                        detail_soup3 = BeautifulSoup(urlopen(g_url + "gameday_Syn.xml"), features="lxml")
                        if detail_soup3.find("venue"):
                            park_id = detail_soup3.stadium["id"]
                            park_name = detail_soup3.stadium["name"]
                            park_loc = detail_soup3.stadium["location"]
                    else:
                        park_id = "unknown"
                        park_name = "unknown"
                        park_loc = "unknown"
                if BeautifulSoup(urlopen(g_url), features="lxml").find("a", href="gameday_Syn.xml"):
                    detail_soup2 = BeautifulSoup(urlopen(g_url + "gameday_Syn.xml"), features="lxml")
                    if detail_soup2.find("game"):
                        id = detail_soup2.game["id"].replace('/', '')
                        game_id = detail_soup2.game["idpk"]
                    else:
                        id = 'unknown'
            else:
                logging.info(g_url + "game.xml |ERROR: Please Retry To Get Data - 272")
                st_fl = "U"
                regseason_fl = "U"
                playoff_fl = "U"
                game_type = "U"
                game_type_des = "Unknown"
                local_game_time = "Unknown"
                game_id = "Unknown"
                home_team_id = "Unknown"
                away_team_id = "Unknown"
                home_team_lg = "Unknown"
                away_team_lg = "Unknown"
                interleague_fl = "U"
                park_id = "Unknown"
                park_name = "Unknown"
                park_loc = "Unknown"
            retro_game_id = home_team_id.upper() + str(active_date.year) + str(active_date.strftime('%m')) + str(
                active_date.strftime('%d')) + str(int(game_number) - 1)
            inn_url = g_url + "inning/"
            try:
                urlopen(inn_url)
                tested_inn_url = inn_url
            except:
                continue
            for inning in BeautifulSoup(urlopen(tested_inn_url),features="lxml").find_all("a", href=re.compile("inning_\d*.xml")):
                inn_soup = BeautifulSoup(urlopen(inn_url + inning.get_text().strip()), features="lxml")
                inning_number = inn_soup.inning["num"]
                top_outs = 0
                bottom_outs = 0
                if inn_soup.inning.find("top"):
                    for ab in inn_soup.inning.top.find_all("atbat"):
                        pitch_type_seq = ""
                        battedball_cd = ""
                        base1 = "_"
                        base2 = "_"
                        base3 = "_"
                        ball_tally = 0
                        strike_tally = 0
                        pitch_seq = ""
                        if 'b' in ab.attrs:
                            ball_ct = ab["b"]
                        else:
                            ball_ct = ""
                        if 's' in ab.attrs:
                            strike_ct = ab["s"]
                        else:
                            strike_ct = ""
                        if 'o' in ab.attrs:
                            event_outs_ct = str(int(ab["o"]) - top_outs)
                        else:
                            event_outs_ct = ""
                        bat_home_id = 0
                        if 'batter' in ab.attrs:
                            bat_mlbid = ab["batter"]
                        else:
                            bat_mlbid = ""
                        if 'stand' in ab.attrs:
                            bat_hand_cd = ab["stand"]
                        else:
                            bat_hand_cd = ""
                        if 'pitcher' in ab.attrs:
                            pit_mlbid = ab["pitcher"]
                        else:
                            pit_mlbid = ""
                        if 'p_throws' in ab.attrs:
                            pit_hand_cd = ab["p_throws"]
                        else:
                            pit_hand_cd = ""
                        if 'des' in ab.attrs:
                            ab_des = ab["des"]
                        else:
                            ab_des = ""
                        if 'num' in ab.attrs:
                            ab_number = ab["num"]
                        else:
                            ab_number = ""
                        if 'event' in ab.attrs:
                            event_tx = ab["event"]
                        else:
                            event_tx = ""
                        event_cd = ""
                        if event_tx == "Flyout" or event_tx == "Fly Out" or event_tx == "Sac Fly" or event_tx == "Sac Fly DP":
                            event_cd = 2
                            battedball_cd = "F"
                        elif event_tx == "Lineout" or event_tx == "Line Out" or event_tx == "Bunt Lineout":
                            event_cd = 2
                            battedball_cd = "L"
                        elif event_tx == "Pop out" or event_tx == "Pop Out" or event_tx == "Bunt Pop Out":
                            event_cd = 2
                            battedball_cd = "P"
                        elif event_tx == "Groundout" or event_tx == "Ground Out" or event_tx == "Sac Bunt" or event_tx == "Bunt Groundout":
                            event_cd = 2
                            battedball_cd = "G"
                        elif event_tx == "Grounded Into DP":
                            event_cd = 2
                            battedball_cd = "G"
                        elif event_tx == "Forceout":
                            event_cd = 2
                            if ab_des.lower().count("grounds") > 0:
                                battedball_cd = "G"
                            elif ab_des.lower().count("lines") > 0:
                                battedball_cd = "L"
                            elif ab_des.lower().count("flies") > 0:
                                battedball_cd = "F"
                            elif ab_des.lower().count("pops") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Double Play" or event_tx == "Triple Play" or event_tx == "Sacrifice Bunt D":
                            event_cd = 2
                            if ab_des.lower().count("ground") > 0:
                                battedball_cd = "G"
                            elif ab_des.lower().count("lines") > 0:
                                battedball_cd = "L"
                            elif ab_des.lower().count("flies") > 0:
                                battedball_cd = "F"
                            elif ab_des.lower().count("pops") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Strikeout" or event_tx == "Strikeout - DP":
                            event_cd = 3
                        elif event_tx == "Walk":
                            event_cd = 14
                        elif event_tx == "Intent Walk":
                            event_cd = 15
                        elif event_tx == "Hit By Pitch":
                            event_cd = 16
                        elif event_tx.lower().count("interference") > 0:
                            event_cd = 17
                        elif event_tx[-5:] == "Error":
                            event_cd = 18
                        elif event_tx == "Fielders Choice Out" or event_tx == "Fielders Choice":
                            event_cd = 19
                        elif event_tx == "Single":
                            event_cd = 20
                            if ab_des.count("on a line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Double":
                            event_cd = 21
                            if ab_des.count("line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Triple":
                            event_cd = 22
                            if ab_des.count("line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Home Run":
                            event_cd = 23
                            if ab_des.count("on a line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Runner Out":
                            if ab_des.lower().count("caught stealing") > 0:
                                event_cd = 6
                            elif ab_des.lower().count("picks off") > 0:
                                event_cd = 8
                        else:
                            event_cd = 99
                        if ab.find("runner", start="1B"):
                            base1 = "1"
                        if ab.find("runner", start="2B"):
                            base2 = "2"
                        if ab.find("runner", start="3B"):
                            base3 = "3"
                        base_state_tx = base1 + base2 + base3
                        if base_state_tx == "___":
                            start_bases_cd = "0"
                        elif base_state_tx == "1__":
                            start_bases_cd = "1"
                        elif base_state_tx == "_2_":
                            start_bases_cd = "2"
                        elif base_state_tx == "12_":
                            start_bases_cd = "3"
                        elif base_state_tx == "__3":
                            start_bases_cd = "4"
                        elif base_state_tx == "1_3":
                            start_bases_cd = "5"
                        elif base_state_tx == "_23":
                            start_bases_cd = "6"
                        elif base_state_tx == "123":
                            start_bases_cd = "7"
                        else:
                            start_bases_cd = "9"
                        base1 = "_"
                        base2 = "_"
                        base3 = "_"
                        if ab.find("runner", end="1B"):
                            base1 = "1"
                        if ab.find("runner", end="2B"):
                            base2 = "2"
                        if ab.find("runner", end="3B"):
                            base3 = "3"
                        base_state_tx = base1 + base2 + base3
                        if base_state_tx == "___":
                            end_bases_cd = "0"
                        elif base_state_tx == "1__":
                            end_bases_cd = "1"
                        elif base_state_tx == "_2_":
                            end_bases_cd = "2"
                        elif base_state_tx == "12_":
                            end_bases_cd = "3"
                        elif base_state_tx == "__3":
                            end_bases_cd = "4"
                        elif base_state_tx == "1_3":
                            end_bases_cd = "5"
                        elif base_state_tx == "_23":
                            end_bases_cd = "6"
                        elif base_state_tx == "123":
                            end_bases_cd = "7"
                        else:
                            end_bases_cd = "9"
                        for pitch in ab.find_all("pitch"):
                            pa_terminal_fl = "U"
                            comp_ct = 0
                            if 'type' in pitch.attrs:
                                pitch_res = pitch["type"]
                                comp_ct += 1
                            else:
                                pitch_res = ""
                            if 'des' in pitch.attrs:
                                pitch_des = pitch["des"]
                                comp_ct += 1
                            else:
                                pitch_des = ""
                            if pitch_des == "Foul":
                                pitch_res = "F"
                            if pitch_des == "Called Strike":
                                pitch_res = "C"
                            if 'id' in pitch.attrs:
                                pitch_id = pitch["id"]
                                comp_ct += 1
                            else:
                                pitch_id = ""
                            pitch_seq += pitch_res
                            if pitch_res == "X" or (
                                    (pitch_res == "S" or pitch_res == "C") and event_cd == 3 and strike_tally == 2) or (
                                    ball_tally == 3 and pitch_res == "B" and (event_cd == 14 or event_cd == 15)):
                                pa_terminal_fl = "T"
                            else:
                                pa_terminal_fl = "F"
                            if 'x' in pitch.attrs:
                                x = pitch["x"]
                                comp_ct += 1
                            else:
                                x = ""
                            if 'y' in pitch.attrs:
                                pitch_y = pitch["y"]
                                comp_ct += 1
                            else:
                                pitch_y = ""
                            if 'sv_id' in pitch.attrs:
                                sv_id = pitch["sv_id"]
                                comp_ct += 1
                            else:
                                sv_id = ""
                            if 'start_speed' in pitch.attrs:
                                start_speed = pitch["start_speed"]
                                comp_ct += 1
                            else:
                                start_speed = ""
                            if 'end_speed' in pitch.attrs:
                                end_speed = pitch["end_speed"]
                                comp_ct += 1
                            else:
                                end_speed = ""
                            if 'sz_top' in pitch.attrs:
                                sz_top = pitch["sz_top"]
                                comp_ct += 1
                            else:
                                sz_top = ""
                            if 'sz_bot' in pitch.attrs:
                                sz_bot = pitch["sz_bot"]
                                comp_ct += 1
                            else:
                                sz_bot = ""
                            if 'pfx_x' in pitch.attrs:
                                pfx_x = pitch["pfx_x"]
                                comp_ct += 1
                            else:
                                pfx_x = ""
                            if 'pfx_z' in pitch.attrs:
                                pfx_z = pitch["pfx_z"]
                                comp_ct += 1
                            else:
                                pfx_z = ""
                            if 'px' in pitch.attrs:
                                px = pitch["px"]
                                comp_ct += 1
                            else:
                                px = ""
                            if 'pz' in pitch.attrs:
                                pz = pitch["pz"]
                                comp_ct += 1
                            else:
                                pz = ""
                            if 'x0' in pitch.attrs:
                                x0 = pitch["x0"]
                                comp_ct += 1
                            else:
                                x0 = ""
                            if 'y0' in pitch.attrs:
                                y0 = pitch["y0"]
                                comp_ct += 1
                            else:
                                y0 = ""
                            if 'z0' in pitch.attrs:
                                z0 = pitch["z0"]
                                comp_ct += 1
                            else:
                                z0 = ""
                            if 'vx0' in pitch.attrs:
                                vx0 = pitch["vx0"]
                                comp_ct += 1
                            else:
                                vx0 = ""
                            if 'vy0' in pitch.attrs:
                                vy0 = pitch["vy0"]
                                comp_ct += 1
                            else:
                                vy0 = ""
                            if 'vz0' in pitch.attrs:
                                vz0 = pitch["vz0"]
                                comp_ct += 1
                            else:
                                vz0 = ""
                            if 'ax' in pitch.attrs:
                                ax = pitch["ax"]
                                comp_ct += 1
                            else:
                                ax = ""
                            if 'ay' in pitch.attrs:
                                ay = pitch["ay"]
                                comp_ct += 1
                            else:
                                ay = ""
                            if 'az' in pitch.attrs:
                                az = pitch["az"]
                                comp_ct += 1
                            else:
                                az = ""
                            if 'break_y' in pitch.attrs:
                                break_y = pitch["break_y"]
                                comp_ct += 1
                            else:
                                break_y = ""
                            if 'break_angle' in pitch.attrs:
                                break_angle = pitch["break_angle"]
                                comp_ct += 1
                            else:
                                break_angle = ""
                            if 'break_length' in pitch.attrs:
                                break_length = pitch["break_length"]
                                comp_ct += 1
                            else:
                                break_length = ""
                            if 'pitch_type' in pitch.attrs:
                                pitch_type = pitch["pitch_type"]
                                comp_ct += 1
                            else:
                                pitch_type = ""
                            if pitch_type_seq == "":
                                pitch_type_seq += pitch_type
                            else:
                                pitch_type_seq += ("|" + pitch_type)
                            if 'type_confidence' in pitch.attrs:
                                type_conf = pitch["type_confidence"]
                                comp_ct += 1
                            else:
                                type_conf = ""
                            if 'zone' in pitch.attrs:
                                zone = pitch["zone"]
                                comp_ct += 1
                            else:
                                zone = ""
                            if 'spin_dir' in pitch.attrs:
                                spin_dir = pitch["spin_dir"]
                                comp_ct += 1
                            else:
                                spin_dir = ""
                            if 'spin_rate' in pitch.attrs:
                                spin_rate = pitch["spin_rate"]
                                comp_ct += 1
                            else:
                                spin_rate = ""
                            pitch_outfile.write(
                                str(retro_game_id) + "," + str(id) + "," + str(active_date.year) + "," + str(st_fl) + "," + str(
                                    regseason_fl) + "," + str(playoff_fl) + "," + str(game_type) + "," + str(
                                    game_type_des) + "," + str(game_id) + "," + str(home_team_id) + "," + str(
                                    home_team_lg) + "," + str(away_team_id) + "," + str(away_team_lg) + "," + str(
                                    interleague_fl) + "," + str(inning_number) + "," + str(bat_home_id) + "," + str(
                                    park_id) + "," + str(park_name) + ",\"" + str(park_loc) + "\"," + str(
                                    pit_mlbid) + "," + str(bat_mlbid) + "," + str(pit_hand_cd) + "," + str(
                                    bat_hand_cd) + "," + str(ball_tally) + "," + str(strike_tally) + "," + str(
                                    top_outs) + "," + str(pitch_seq) + "," + str(pa_terminal_fl) + "," + str(
                                    event_cd) + "," + str(start_bases_cd) + "," + str(end_bases_cd) + "," + str(
                                    event_outs_ct) + "," + str(ab_number) + "," + str(pitch_res) + ",\"" + str(
                                    pitch_des) + "\"," + str(pitch_id) + "," + str(x) + "," + str(pitch_y) + "," + str(
                                    start_speed) + "," + str(end_speed) + "," + str(sz_top) + "," + str(
                                    sz_bot) + "," + str(pfx_x) + "," + str(pfx_z) + "," + str(px) + "," + str(
                                    pz) + "," + str(x0) + "," + str(y0) + "," + str(z0) + "," + str(vx0) + "," + str(
                                    vy0) + "," + str(vz0) + "," + str(ax) + "," + str(ay) + "," + str(az) + "," + str(
                                    break_y) + "," + str(break_angle) + "," + str(break_length) + "," + str(
                                    pitch_type) + "," + str(pitch_type_seq) + "," + str(type_conf) + "," + str(
                                    zone) + "," + str(spin_dir) + "," + str(spin_rate) + "," + str(sv_id) + "\n")
                            if pitch_res == "B":
                                if ball_tally < 4:
                                    ball_tally += 1
                            elif pitch_res == "S" or pitch_res == "C" or pitch_res == "X":
                                if strike_tally < 3:
                                    strike_tally += 1
                            elif pitch_res == "F":
                                if strike_tally < 2:
                                    strike_tally += 1
                        atbat_outfile.write(
                            str(retro_game_id) + "," + str(id) + "," + str(active_date.year) + "," + str(active_date.month) + "," + str(
                                active_date.day) + "," + str(st_fl) + "," + str(regseason_fl) + "," + str(
                                playoff_fl) + "," + str(game_type) + "," + str(game_type_des) + "," + str(
                                local_game_time) + "," + str(game_id) + "," + str(home_team_id) + "," + str(
                                away_team_id) + "," + str(home_team_lg) + "," + str(away_team_lg) + "," + str(
                                interleague_fl) + "," + str(park_id) + "," + str(park_name) + ",\"" + str(
                                park_loc) + "\"," + str(inning_number) + "," + str(bat_home_id) + "," + str(
                                top_outs) + "," + str(ab_number) + "," + str(pit_mlbid) + "," + str(
                                pit_hand_cd) + "," + str(bat_mlbid) + "," + str(bat_hand_cd) + "," + str(
                                ball_ct) + "," + str(strike_ct) + "," + str(pitch_seq) + "," + str(
                                pitch_type_seq) + "," + str(event_outs_ct) + ",\"" + str(ab_des) + "\"," + str(
                                event_tx) + "," + str(event_cd) + "," + str(battedball_cd) + "," + str(
                                start_bases_cd) + "," + str(end_bases_cd) + "\n")
                        top_outs += int(event_outs_ct)
                if inn_soup.inning.find("bottom"):
                    for ab in inn_soup.inning.bottom.find_all("atbat"):
                        pitch_type_seq = ""
                        battedball_cd = ""
                        base1 = "_"
                        base2 = "_"
                        base3 = "_"
                        ball_tally = 0
                        strike_tally = 0
                        pitch_seq = ""
                        if 'b' in ab.attrs:
                            ball_ct = ab["b"]
                        else:
                            ball_ct = ""
                        if 's' in ab.attrs:
                            strike_ct = ab["s"]
                        else:
                            strike_ct = ""
                        if 'o' in ab.attrs:
                            event_outs_ct = str(int(ab["o"]) - bottom_outs)
                        else:
                            event_outs_ct = ""
                        bat_home_id = 1
                        if 'batter' in ab.attrs:
                            bat_mlbid = ab["batter"]
                        else:
                            bat_mlbid = ""
                        if 'stand' in ab.attrs:
                            bat_hand_cd = ab["stand"]
                        else:
                            bat_hand_cd = ""
                        if 'pitcher' in ab.attrs:
                            pit_mlbid = ab["pitcher"]
                        else:
                            pit_mlbid = ""
                        if 'p_throws' in ab.attrs:
                            pit_hand_cd = ab["p_throws"]
                        else:
                            pit_hand_cd = ""
                        if 'des' in ab.attrs:
                            ab_des = ab["des"]
                        else:
                            ab_des = ""
                        if 'num' in ab.attrs:
                            ab_number = ab["num"]
                        else:
                            ab_number = ""
                        if 'event' in ab.attrs:
                            event_tx = ab["event"]
                        else:
                            event_tx = ""
                        if event_tx == "Flyout" or event_tx == "Fly Out" or event_tx == "Sac Fly" or event_tx == "Sac Fly DP":
                            event_cd = 2
                            battedball_cd = "F"
                        elif event_tx == "Lineout" or event_cd == "Line Out" or event_tx == "Bunt Lineout":
                            event_cd = 2
                            battedball_cd = "L"
                        elif event_tx == "Pop out" or event_tx == "Pop Out" or event_tx == "Bunt Pop Out":
                            event_cd = 2
                            battedball_cd = "P"
                        elif event_tx == "Groundout" or event_tx == "Ground Out" or event_tx == "Sac Bunt" or event_tx == "Bunt Groundout":
                            event_cd = 2
                            battedball_cd = "G"
                        elif event_tx == "Grounded Into DP":
                            event_cd = 2
                            battedball_cd = "G"
                        elif event_tx == "Forceout" or event_tx == "Force Out":
                            event_cd = 2
                            if ab_des.lower().count("grounds") > 0:
                                battedball_cd = "G"
                            elif ab_des.lower().count("lines") > 0:
                                battedball_cd = "L"
                            elif ab_des.lower().count("flies") > 0:
                                battedball_cd = "F"
                            elif ab_des.lower().count("pops") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Double Play" or event_tx == "Triple Play" or event_tx == "Sacrifice Bunt D":
                            event_cd = 2
                            if ab_des.lower().count("ground") > 0:
                                battedball_cd = "G"
                            elif ab_des.lower().count("lines") > 0:
                                battedball_cd = "L"
                            elif ab_des.lower().count("flies") > 0:
                                battedball_cd = "F"
                            elif ab_des.lower().count("pops") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Strikeout" or event_tx == "Strikeout - DP":
                            event_cd = 3
                        elif event_tx == "Walk":
                            event_cd = 14
                        elif event_tx == "Intent Walk":
                            event_cd = 15
                        elif event_tx == "Hit By Pitch":
                            event_cd = 16
                        elif event_tx.lower().count("interference") > 0:
                            event_cd = 17
                        elif event_tx[-5:] == "Error":
                            event_cd = 18
                        elif event_tx == "Fielders Choice Out" or event_tx == "Fielders Choice":
                            event_cd = 19
                        elif event_tx == "Single":
                            event_cd = 20
                            if ab_des.count("on a line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Double":
                            event_cd = 21
                            if ab_des.count("line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Triple":
                            event_cd = 22
                            if ab_des.count("line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Home Run":
                            event_cd = 23
                            if ab_des.count("on a line drive") > 0:
                                battedball_cd = "L"
                            elif ab_des.count("fly ball") > 0:
                                battedball_cd = "F"
                            elif ab_des.count("ground ball") > 0:
                                battedball_cd = "G"
                            elif ab_des.count("pop up") > 0:
                                battedball_cd = "P"
                            else:
                                battedball_cd = ""
                        elif event_tx == "Runner Out":
                            if ab_des.lower().count("caught stealing") > 0:
                                event_cd = 6
                            elif ab_des.lower().count("picks off") > 0:
                                event_cd = 8
                        else:
                            event_cd = 99
                        if ab.find("runner", start="1B"):
                            base1 = "1"
                        if ab.find("runner", start="2B"):
                            base2 = "2"
                        if ab.find("runner", start="3B"):
                            base3 = "3"
                        base_state_tx = base1 + base2 + base3
                        if base_state_tx == "___":
                            start_bases_cd = "0"
                        elif base_state_tx == "1__":
                            start_bases_cd = "1"
                        elif base_state_tx == "_2_":
                            start_bases_cd = "2"
                        elif base_state_tx == "12_":
                            start_bases_cd = "3"
                        elif base_state_tx == "__3":
                            start_bases_cd = "4"
                        elif base_state_tx == "1_3":
                            start_bases_cd = "5"
                        elif base_state_tx == "_23":
                            start_bases_cd = "6"
                        elif base_state_tx == "123":
                            start_bases_cd = "7"
                        else:
                            start_bases_cd = "9"
                        base1 = "_"
                        base2 = "_"
                        base3 = "_"
                        if ab.find("runner", end="1B"):
                            base1 = "1"
                        if ab.find("runner", end="2B"):
                            base2 = "2"
                        if ab.find("runner", end="3B"):
                            base3 = "3"
                        base_state_tx = base1 + base2 + base3
                        if base_state_tx == "___":
                            end_bases_cd = "0"
                        elif base_state_tx == "1__":
                            end_bases_cd = "1"
                        elif base_state_tx == "_2_":
                            end_bases_cd = "2"
                        elif base_state_tx == "12_":
                            end_bases_cd = "3"
                        elif base_state_tx == "__3":
                            end_bases_cd = "4"
                        elif base_state_tx == "1_3":
                            end_bases_cd = "5"
                        elif base_state_tx == "_23":
                            end_bases_cd = "6"
                        elif base_state_tx == "123":
                            end_bases_cd = "7"
                        else:
                            end_bases_cd = "9"
                        for pitch in ab.find_all("pitch"):
                            pa_terminal_fl = "U"
                            comp_ct = 0
                            if 'type' in pitch.attrs:
                                pitch_res = pitch["type"]
                                comp_ct += 1
                            else:
                                pitch_res = ""
                            if 'des' in pitch.attrs:
                                pitch_des = pitch["des"]
                                comp_ct += 1
                            else:
                                pitch_des = ""
                            if pitch_des == "Foul":
                                pitch_res = "F"
                            if pitch_des == "Called Strike":
                                pitch_res = "C"
                            if 'id' in pitch.attrs:
                                pitch_id = pitch["id"]
                                comp_ct += 1
                            else:
                                pitch_id = ""
                            pitch_seq += pitch_res
                            if pitch_res == "X" or (
                                    (pitch_res == "S" or pitch_res == "C") and event_cd == 3 and strike_tally == 2) or (
                                    pitch_res == "B" and (event_cd == 14 or event_cd == 15) and ball_tally == 3):
                                pa_terminal_fl = "T"
                            else:
                                pa_terminal_fl = "F"
                            if 'x' in pitch.attrs:
                                x = pitch["x"]
                                comp_ct += 1
                            else:
                                x = ""
                            if 'y' in pitch.attrs:
                                pitch_y = pitch["y"]
                                comp_ct += 1
                            else:
                                pitch_y = ""
                            if 'sv_id' in pitch.attrs:
                                sv_id = pitch["sv_id"]
                                comp_ct += 1
                            else:
                                sv_id = ""
                            if 'start_speed' in pitch.attrs:
                                start_speed = pitch["start_speed"]
                                comp_ct += 1
                            else:
                                start_speed = ""
                            if 'end_speed' in pitch.attrs:
                                end_speed = pitch["end_speed"]
                                comp_ct += 1
                            else:
                                end_speed = ""
                            if 'sz_top' in pitch.attrs:
                                sz_top = pitch["sz_top"]
                                comp_ct += 1
                            else:
                                sz_top = ""
                            if 'sz_bot' in pitch.attrs:
                                sz_bot = pitch["sz_bot"]
                                comp_ct += 1
                            else:
                                sz_bot = ""
                            if 'pfx_x' in pitch.attrs:
                                pfx_x = pitch["pfx_x"]
                                comp_ct += 1
                            else:
                                pfx_x = ""
                            if 'pfx_z' in pitch.attrs:
                                pfx_z = pitch["pfx_z"]
                                comp_ct += 1
                            else:
                                pfx_z = ""
                            if 'px' in pitch.attrs:
                                px = pitch["px"]
                                comp_ct += 1
                            else:
                                px = ""
                            if 'pz' in pitch.attrs:
                                pz = pitch["pz"]
                                comp_ct += 1
                            else:
                                pz = ""
                            if 'x0' in pitch.attrs:
                                x0 = pitch["x0"]
                                comp_ct += 1
                            else:
                                x0 = ""
                            if 'y0' in pitch.attrs:
                                y0 = pitch["y0"]
                                comp_ct += 1
                            else:
                                y0 = ""
                            if 'z0' in pitch.attrs:
                                z0 = pitch["z0"]
                                comp_ct += 1
                            else:
                                z0 = ""
                            if 'vx0' in pitch.attrs:
                                vx0 = pitch["vx0"]
                                comp_ct += 1
                            else:
                                vx0 = ""
                            if 'vy0' in pitch.attrs:
                                vy0 = pitch["vy0"]
                                comp_ct += 1
                            else:
                                vy0 = ""
                            if 'vz0' in pitch.attrs:
                                vz0 = pitch["vz0"]
                                comp_ct += 1
                            else:
                                vz0 = ""
                            if 'ax' in pitch.attrs:
                                ax = pitch["ax"]
                                comp_ct += 1
                            else:
                                ax = ""
                            if 'ay' in pitch.attrs:
                                ay = pitch["ay"]
                                comp_ct += 1
                            else:
                                ay = ""
                            if 'az' in pitch.attrs:
                                az = pitch["az"]
                                comp_ct += 1
                            else:
                                az = ""
                            if 'break_y' in pitch.attrs:
                                break_y = pitch["break_y"]
                                comp_ct += 1
                            else:
                                break_y = ""
                            if 'break_angle' in pitch.attrs:
                                break_angle = pitch["break_angle"]
                                comp_ct += 1
                            else:
                                break_angle = ""
                            if 'break_length' in pitch.attrs:
                                break_length = pitch["break_length"]
                                comp_ct += 1
                            else:
                                break_length = ""
                            if 'pitch_type' in pitch.attrs:
                                pitch_type = pitch["pitch_type"]
                                comp_ct += 1
                            else:
                                pitch_type = ""
                            if pitch_type_seq == "":
                                pitch_type_seq += pitch_type
                            else:
                                pitch_type_seq += ("|" + pitch_type)
                            if 'type_confidence' in pitch.attrs:
                                type_conf = pitch["type_confidence"]
                                comp_ct += 1
                            else:
                                type_conf = ""
                            if 'zone' in pitch.attrs:
                                zone = pitch["zone"]
                                comp_ct += 1
                            else:
                                zone = ""
                            if 'spin_dir' in pitch.attrs:
                                spin_dir = pitch["spin_dir"]
                                comp_ct += 1
                            else:
                                spin_dir = ""
                            if 'spin_rate' in pitch.attrs:
                                spin_rate = pitch["spin_rate"]
                                comp_ct += 1
                            else:
                                spin_rate = ""
                            pitch_outfile.write(
                                str(retro_game_id) + "," + str(id) + "," + str(active_date.year) + "," + str(st_fl) + "," + str(
                                    regseason_fl) + "," + str(playoff_fl) + "," + str(game_type) + "," + str(
                                    game_type_des) + "," + str(game_id) + "," + str(home_team_id) + "," + str(
                                    home_team_lg) + "," + str(away_team_id) + "," + str(away_team_lg) + "," + str(
                                    interleague_fl) + "," + str(inning_number) + "," + str(bat_home_id) + "," + str(
                                    park_id) + "," + str(park_name) + ",\"" + str(park_loc) + "\"," + str(
                                    pit_mlbid) + "," + str(bat_mlbid) + "," + str(pit_hand_cd) + "," + str(
                                    bat_hand_cd) + "," + str(ball_tally) + "," + str(strike_tally) + "," + str(
                                    bottom_outs) + "," + str(pitch_seq) + "," + str(pa_terminal_fl) + "," + str(
                                    event_cd) + "," + str(start_bases_cd) + "," + str(end_bases_cd) + "," + str(
                                    event_outs_ct) + "," + str(ab_number) + "," + str(pitch_res) + ",\"" + str(
                                    pitch_des) + "\"," + str(pitch_id) + "," + str(x) + "," + str(pitch_y) + "," + str(
                                    start_speed) + "," + str(end_speed) + "," + str(sz_top) + "," + str(
                                    sz_bot) + "," + str(pfx_x) + "," + str(pfx_z) + "," + str(px) + "," + str(
                                    pz) + "," + str(x0) + "," + str(y0) + "," + str(z0) + "," + str(vx0) + "," + str(
                                    vy0) + "," + str(vz0) + "," + str(ax) + "," + str(ay) + "," + str(az) + "," + str(
                                    break_y) + "," + str(break_angle) + "," + str(break_length) + "," + str(
                                    pitch_type) + "," + str(pitch_type_seq) + "," + str(type_conf) + "," + str(
                                    zone) + "," + str(spin_dir) + "," + str(spin_rate) + "," + str(sv_id) + "\n")
                            if pitch_res == "B":
                                if ball_tally < 4:
                                    ball_tally += 1
                            elif pitch_res == "S" or pitch_res == "C" or pitch_res == "X":
                                if strike_tally < 3:
                                    strike_tally += 1
                            elif pitch_res == "F":
                                if strike_tally < 2:
                                    strike_tally += 1
                        atbat_outfile.write(
                            str(retro_game_id) + "," + str(id) + "," + str(active_date.year) + "," + str(active_date.month) + "," + str(
                                active_date.day) + "," + str(st_fl) + "," + str(regseason_fl) + "," + str(
                                playoff_fl) + "," + str(game_type) + "," + str(game_type_des) + "," + str(
                                local_game_time) + "," + str(game_id) + "," + str(home_team_id) + "," + str(
                                away_team_id) + "," + str(home_team_lg) + "," + str(away_team_lg) + "," + str(
                                interleague_fl) + "," + str(park_id) + "," + str(park_name) + ",\"" + str(
                                park_loc) + "\"," + str(inning_number) + "," + str(bat_home_id) + "," + str(
                                bottom_outs) + "," + str(ab_number) + "," + str(pit_mlbid) + "," + str(
                                pit_hand_cd) + "," + str(bat_mlbid) + "," + str(bat_hand_cd) + "," + str(
                                ball_ct) + "," + str(strike_ct) + "," + str(pitch_seq) + "," + str(
                                pitch_type_seq) + "," + str(event_outs_ct) + ",\"" + str(ab_des) + "\"," + str(
                                event_tx) + "," + str(event_cd) + "," + str(battedball_cd) + "," + str(
                                start_bases_cd) + "," + str(end_bases_cd) + "\n")
                        bottom_outs += int(event_outs_ct)
        prior_d_url = d_url
#Import atbats and pitches csv files to MySQL Database: Note Tables (pitchfx.pitches & pitchfx.atbats) in MySQL DB must already be created - see SQL Scripts
icsv.importfile(prefix)
