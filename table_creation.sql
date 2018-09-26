CREATE TABLE `pitches` (
  `index` bigint(20) DEFAULT NULL,
  `retro_game_id` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `st_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `regseason_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `playoffs_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `game_type` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `game_type_des` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `game_id` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `home_team_id` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `home_team_lg` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `away_team_id` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `away_team_lg` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `interleague_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `inning` int(11) DEFAULT NULL,
  `bat_home_id` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `park_id` int(11) DEFAULT NULL,
  `park_name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `park_loc` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pit_id` int(11) DEFAULT NULL,
  `bat_id` int(11) DEFAULT NULL,
  `pit_hand_cd` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bat_hand_cd` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pa_ball_ct` int(11) DEFAULT NULL,
  `pa_strike_ct` int(11) DEFAULT NULL,
  `outs_ct` int(11) DEFAULT NULL,
  `pitch_seq` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pa_terminal_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pa_event_cd` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_bases_cd` int(11) DEFAULT NULL,
  `end_bases_cd` int(11) DEFAULT NULL,
  `event_outs_ct` int(11) DEFAULT NULL,
  `ab_number` int(11) DEFAULT NULL,
  `pitch_res` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pitch_des` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pitch_id` int(11) DEFAULT NULL,
  `x` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `y` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_speed` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `end_speed` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sz_top` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sz_bot` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pfx_x` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pfx_z` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `px` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pz` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `x0` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `y0` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `z0` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vx0` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vy0` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vz0` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ax` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ay` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `az` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `break_y` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `break_angle` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `break_length` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pitch_type` varchar(2) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pitch_type_seq` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type_conf` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `zone` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `spin_dir` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `spin_rate` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL,
  `sv_id` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  KEY `index_pitches_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `atbats` (
  `index` bigint(20) DEFAULT NULL,
  `retro_game_id` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `month` int(11) DEFAULT NULL,
  `day` int(11) DEFAULT NULL,
  `st_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `regseason_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `playoff_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `game_type` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `game_type_des` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `local_game_time` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `game_id` varchar(7) COLLATE utf8_unicode_ci DEFAULT NULL,
  `home_team_id` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `away_team_id` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `home_team_lg` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `away_team_lg` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `interleague_fl` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `park_id` int(11) DEFAULT NULL,
  `park_name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `park_location` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `inning_number` int(11) DEFAULT NULL,
  `bat_home_id` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `inn_outs` int(11) DEFAULT NULL,
  `ab_number` int(11) DEFAULT NULL,
  `pit_mlbid` int(11) DEFAULT NULL,
  `pit_hand_cd` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `bat_mlbid` int(11) DEFAULT NULL,
  `bat_hand_cd` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ball_ct` int(11) DEFAULT NULL,
  `strike_ct` int(11) DEFAULT NULL,
  `pitch_seq` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pitch_type_seq` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_outs_ct` int(11) DEFAULT NULL,
  `ab_des` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_tx` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_cd` int(11) DEFAULT NULL,
  `battedball_cd` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_bases_cd` int(11) DEFAULT NULL,
  `end_bases_cd` int(11) DEFAULT NULL,
  KEY `ix_atbats_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
