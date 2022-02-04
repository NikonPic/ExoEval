from exoskeleton.exo_workflow import KinExoParams


def get_model_by_filename(filename: str):
    """set the model by filename"""
    params = get_params_by_name(filename)
    model = KinExoParams()
    model.set_individual_params(params)
    return model


def get_params_by_name(filename: str):
    """return the parameters depending on the filename"""

    if 'niko' in filename:
        return niko_params()

    if 'tina' in filename:
        return tina_params()

    if 'chrissi' in filename:
        return chrissi_params()

    if 'pat2' in filename:
        return pat2_params()

    if 'pat3' in filename:
        return pat3_params()

    if 'pat4' in filename:
        return pat4_params()

    return mech_finger_params()


def new_config_params(params: dict):
    # Gliedlaengen Kinematik (s.Skizze)
    params['l_9'] = 8

    # Bezeichnet die Länge von Aktorverbund in minimal ausgefahrener Länge (Aktorlänge plus Länge Kraftsensorverbund)
    params['l_akt'] = 102 + 36.1

    # Aktorgelenkmountposition hinten relativ zu Gelenk B
    params['akt_x'] = -152.12
    params['akt_y'] = -21.79

    # overall finger length:
    # print('Length_FINGER:', round(
    #     params['l_pp'] + params['l_pm'] + params['l_pd']))

    return params


def apply_reference(params, ref_l8, l8_true=34):
    """
    apply the true length on the params
    """
    factor = l8_true / ref_l8

    for loc_key in params.keys():
        if type(params[loc_key]) == list:
            params[loc_key] = [params[loc_key][idx] *
                               factor for idx in range(len(params[loc_key]))]
            # print(f'{loc_key}: {params[loc_key]}')
        else:
            params[loc_key] = params[loc_key] * factor
            # print(f'{loc_key}: {round(params[loc_key])}')

    return params


def niko_params():
    """Nikos Finger
    measurement in reference sys
    """
    params = {}

    # Phalanges:
    params['l_pp'] = 106.54
    params['l_pm'] = 69.07
    params['l_pd'] = 65.33

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_ap'] = 0  # we use the whole at once
    params['h_pp'] = 42.53
    params['h_pm'] = 27.71
    params['h_pd'] = 48.27

    params['d_gen'] = 33.99

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [17.83, 51.51]

    # define reference and transform to standard_len
    ref_l8 = 88.27
    params = apply_reference(params, ref_l8)

    # define the l_act and l9 new
    params = new_config_params(params)

    return params


def tina_params():
    """Tinas Finger"""
    params = {}

    # Phalanges:
    params['l_pp'] = 84.30
    params['l_pm'] = 50.92
    params['l_pd'] = 52.51

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_ap'] = 0  # we use the whole at once
    params['h_pp'] = 26.37
    params['h_pm'] = 22.33
    params['h_pd'] = 22.79

    params['d_gen'] = 31.72

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [19.65, 33.99]

    # define reference and transform to standard_len
    ref_l8 = 73.35
    params = apply_reference(params, ref_l8)

    # define the l_act and l9 new
    params = new_config_params(params)

    return params


def chrissi_params():
    """Chrissis Finger
    measurement in reference sys
    """
    params = {}

    # Phalanges:
    params['l_pp'] = 89.59
    params['l_pm'] = 57.19
    params['l_pd'] = 56.28

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_ap'] = 0  # we use the whole at once
    params['h_pp'] = 31.48
    params['h_pm'] = 33.83
    params['h_pd'] = 28.04

    params['d_gen'] = 34.51

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [19.62, 42.09]

    # define reference and transform to standard_len
    ref_l8 = 81.32
    params = apply_reference(params, ref_l8)

    # define the l_act and l9 new
    params = new_config_params(params)

    return params


def pat2_params():
    """Finger"""
    params = {}

    # Phalanges:
    params['l_pp'] = 149.70
    params['l_pm'] = 67.79
    params['l_pd'] = 69.98

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_ap'] = 0  # we use the whole at once
    params['h_pp'] = 54.27
    params['h_pm'] = 52.29
    params['h_pd'] = 40.67

    params['d_gen'] = 49.16

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [41.01, 77.75]

    # define reference and transform to standard_len
    ref_l8 = 120.07
    params = apply_reference(params, ref_l8)

    # define the l_act and l9 new
    params = new_config_params(params)

    return params


def pat3_params():
    """Finger"""
    params = {}

    # Phalanges:
    params['l_pp'] = 151.01
    params['l_pm'] = 94.69
    params['l_pd'] = 97.63

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_ap'] = 0  # we use the whole at once
    params['h_pp'] = 65.17
    params['h_pm'] = 64.49
    params['h_pd'] = 49.97

    params['d_gen'] = 36.36

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [41.16, 87.10]

    # define reference and transform to standard_len
    ref_l8 = 148.90
    params = apply_reference(params, ref_l8)

    # define the l_act and l9 new
    params = new_config_params(params)

    return params


def pat4_params():
    """Finger"""
    params = {}

    # Phalanges:
    params['l_pp'] = 226.48
    params['l_pm'] = 145.89
    params['l_pd'] = 144.33

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_ap'] = 0  # we use the whole at once
    params['h_pp'] = 75.45
    params['h_pm'] = 80.92
    params['h_pd'] = 58.97

    params['d_gen'] = 60.74

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [49.78, 119.35]

    # define reference and transform to standard_len
    ref_l8 = 184.63
    params = apply_reference(params, ref_l8)

    # define the l_act and l9 new
    params = new_config_params(params)

    return params


def mech_finger_params():
    """The Mechanical Finger"""
    params = {}

    # Phalanges:
    params['l_pp'] = 45
    params['l_pm'] = 25
    params['l_pd'] = 22.5

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    params['h_pp'] = 8
    params['h_pm'] = 7
    params['h_pd'] = 7

    params['d_gen'] = 12

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    params['A'] = [-2.952, 16.7417]

    # Gliedlaengen Kinematik (s.Skizze)
    params['l_9'] = 10  # new: 8

    # Bezeichnet die Länge von Aktorverbund in minimal ausgefahrener Länge (Aktorlänge plus Länge Kraftsensorverbund)
    params['l_akt'] = 102 + 37.3

    # Aktorgelenkmountposition hinten relativ zu Gelenk B
    params['akt_x'] = -160.761
    params['akt_y'] = -9.845

    return params
