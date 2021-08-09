# %% imports
from math import sqrt, acos, pi, cos, sin, atan

# %% general funtions


def get_angle(p1_x, p1_y, p2_x, p2_y):
    """
    DIRECTION - finds the angle of a vector (r_i) in the worldframe
    Based on two points in space, the angle of the vector representing the positive direction of a linkage rod with respect to
    the positive z-axis of the world frame is found. The direction of the linkage rod
    coincides with the positive force direction transmitted across it. 
    The functions inputs are two vectors with pj[pj_x;pj_y] respectively
    """
    # Calculating the vector r from p1 to p1
    delta_x = p2_x - p1_x
    delta_y = p2_y - p1_y

    # Angle of vector r in worldframe
    if delta_x > 0:
        phi = atan(delta_y/delta_x)
    elif delta_x < 0:
        phi = atan(delta_y/delta_x) - pi
    elif (delta_x == 0) and (delta_y > 0):
        phi = pi/2
    elif (delta_x == 0) and (delta_y < 0):
        phi = -pi/2

    return phi


def get_point(a_x, a_y, l_1, b_x, b_y, l_2):
    """
    getPoint bestimmt die Position eines Gelenks im Weltsystem
    Bei Wahl A_x < B_x im Weltsystem wird oberer Schnittpunkt ausgegeben. Konfiguration "+sqrt(...)" liefert
    C oberhalb von A und B, "-sqrt(...)" liefert C unterhalb von A und B
    Werden A und B in umgekehrter Reihenfolge übergeben liefert Funktion ebenfalls die untere Loesung fuer C 
    """

    A = b_x-a_x
    B = b_y-a_y
    C_A = (A**2 + B**2 + l_1**2 - l_2**2)/(2*l_1)

    # Winkel zwischen x-Achse Weltsystem und Vektor BC = alpha
    # Quadratische Gleichung mit zwei Lösungen, Wahl positive Lösung
    ang_a = 2*atan((B+sqrt(A**2+B**2-C_A**2))/(A+C_A))

    p_x = a_x+cos(ang_a)*l_1
    p_y = a_y+sin(ang_a)*l_1

    return p_x, p_y

# %% Exo Dataclass


class KinExoParams(object):

    # Gliedlaengen Kinematik (s.Skizze)
    l_1 = 45
    l_2 = 35
    l_3 = 31
    l_4 = 22
    l_5 = 15
    l_6 = 25
    l_7 = 38
    l_8 = 34
    l_9 = 10  # new: 8
    l_10 = 38
    l_11 = 23
    l_12 = 28

    # Phalanges:
    l_pp = 45
    l_pm = 25
    l_pd = 22.5

    # Abstand Verbindungsstecke zwischen Fingergelenken zu Oberseite der Fingerglieder
    h_pp = 8
    h_pm = 7
    h_pd = 7

    # Abstand Oberseite der Finger zu Gelenken der Phalanxmodule
    h_ap = 5.5

    # Position Gelenk A: Messen notwendig, Position relativ zu MCP muss bestimmt
    # werden. Hier Werte aus mechanischem Finger gegeben, real aus Foto/Scan
    # bestimmen
    A = [-2.952, 16.7417]

    # >MCP im weltsystem:
    MCP = [0, 0]

    l_g1 = sqrt((0-A[0])**2+(0-A[1])**2)
    psi_2 = acos((-A[0])/l_g1)

    # Konstruktiv definierter Winkel X-Achse zu Strecke AB (in math. pos. Sinn)
    psi_1 = ((180-35)/360)*2*pi

    # Position Gelenk B berechnen
    B = [A[0]+l_5*cos(psi_1), A[1]+l_5*sin(psi_1)]

    # Bezeichnet die Länge von Aktorverbund in minimal ausgefahrener Länge (Aktorlänge plus Länge Kraftsensorverbund)
    l_akt = 102 + 37.3
    akt_x = -160.761  # Aktorgelenkmountposition hinten relativ zu Gelenk B
    akt_y = -9.845  # Aktorgelenkmountposition hinten relativ zu Gelenk B
    theta = (pi/180)*35  # Winkel zwischen kurzer und langer Schwinge in l_1
    l_s = 20  # Laenge der kurzen Schwinge in l_1
    d_b = sqrt((0-akt_x)**2+(0-akt_y)**2)  # Abstand B und Aktoraufhaengung

    # Konstanter Winkel zwischen x-Achse und Verbindungsgraden Gelenk B und Aktoraufhaengung
    alpha_const = pi + get_angle(0, 0, akt_x, akt_y)

    # Laengen bis zu den jeweiligen Schwerpunkten der Finger (s. Skizze) -->
    # Später in Paramterteil definieren!
    l_c1 = l_pp/2
    l_c2 = l_pm/2
    l_c3 = l_pd/2

    # Versatz zwischen jeweiligem Koerperschwerpunkt und den Angriffspunkten der
    # Stabkraefte
    p_11x = 0.5
    p_11y = h_pp + h_ap
    p_12x = 10.5
    p_12y = h_pp + h_ap

    p_2x = 0
    p_2y = h_pm + h_ap

    p_3x = 0
    p_3y = h_pd + h_ap

    # Traegheiten der einzelnen Fingerglieder (Werte aus vereinfachtem CAD Modell)

    # Massen der einzelnen Fingerglieder
    m1 = 0.0
    m2 = 0.0
    m3 = 0.0

    def __init__(self, d_gen=12):
        """init the class"""
        self.get_const_param(d_gen)

    def __call__(self, phi_a, phi_b, phi_k, f_actor) -> list:
        """perform forward call"""
        phi_a *= (pi / 180)
        phi_b *= (pi / 180)
        phi_k *= (pi / 180)

        self.get_kin_config(phi_a, phi_b, phi_k, f_actor)
        return [self.phi_mcp, self.phi_pip, self.phi_dip, self.m_mcp, self.m_pip, self.m_dip]

    def set_individual_params(self, ind_data: dict):
        """set the individual parameters"""

        # iterate trough the individual keys and set the values
        for loc_key in ind_data.keys():
            setattr(self, loc_key, ind_data[loc_key])

        # update params to calculate
        self.l_g1 = sqrt((0-self.A[0])**2+(0-self.A[1])**2)
        self.psi_2 = acos((-self.A[0])/self.l_g1)
        self.B = [self.A[0]+self.l_5 *
                  cos(self.psi_1), self.A[1]+self.l_5*sin(self.psi_1)]
        self.d_b = sqrt((0-self.akt_x)**2+(0-self.akt_y)**2)
        self.alpha_const = pi + get_angle(0, 0, self.akt_x, self.akt_y)
        self.l_c1 = self.l_pp/2
        self.l_c2 = self.l_pm/2
        self.l_c3 = self.l_pd/2
        self.p_11y = self.h_pp + self.h_ap
        self.p_12y = self.h_pp + self.h_ap
        self.p_2y = self.h_pm + self.h_ap
        self.p_3y = self.h_pd + self.h_ap

        # update all further parameters
        self.get_const_param(self.d_gen)

    def get_const_param(self, d_gen):
        """
        getConstParam berechnet die durch den Finger vorgegeben kinematischen
        Parameter bei mittiger Montage der PD und PM Attachments
        Input: Abstand MCP - erstes PP Att. Gelenk
        """
        self.l_g2 = sqrt((self.h_ap + self.h_pp)**2 +
                         (self.l_pp - d_gen - self.l_9)**2)
        self.l_g3 = sqrt((self.h_ap + self.h_pp)**2 + (d_gen)**2)
        self.l_g4 = sqrt((self.h_ap + self.h_pm)**2 + (0.5*self.l_pm)**2)
        self.l_g5 = self.l_g4

        # Bei mittiger Montage gleich
        self.l_g6 = sqrt((self.h_ap + self.h_pd)**2+(0.5*self.l_pd)**2)
        self.psi_6 = acos((self.l_pd/2)/self.l_g6)
        self.psi_5 = acos((self.l_pm/2)/self.l_g4)
        self.psi_4 = acos(d_gen/self.l_g3)
        self.psi_3 = acos((self.l_pp - d_gen - self.l_9)/self.l_g2)

    def get_kin_config(self, phi_a, phi_b, phi_k, f_actor):
        # kinematic config
        self.joint_5_1(phi_a, phi_b)
        self.joint_4_2()
        self.joint_5_3()
        self.joint_5_4(phi_k)
        self.joint_4_5()

        # config 2 angles
        self.get_joint_angles()
        self.get_stab_angles()

        # angles and forces together
        self.get_actuation_force(f_actor)
        self.get_all_rod_forces()
        self.get_joint_torques()

    def joint_5_1(self, phi_a, phi_b):
        """Gelenkfuenfeck 1"""
        c_x = self.B[0]+self.l_1*cos(phi_b)
        c_y = self.B[1]+self.l_1*sin(phi_b)
        C = [c_x, c_y]
        self.C = C

        e_x = self.A[0]+self.l_4*cos(phi_a)
        e_y = self.A[1]+self.l_4*sin(phi_a)
        E = [e_x, e_y]
        self.E = E

        # Zweischlag E-D-C
        d_x, d_y = get_point(C[0], C[1], self.l_2, E[0], E[1], self.l_3)
        D = [d_x, d_y]
        self.D = D

    def joint_4_2(self):
        """Gelenkviereck 2"""
        # Zweischlag E-F-MCP
        f_x, f_y = get_point(
            self.E[0], self.E[1], self.l_6, self.MCP[0], self.MCP[1], self.l_g2)
        F = [f_x, f_y]
        self.F = F

    def joint_5_3(self):
        """Gelenkfuenfeck 3"""
        # Bestimmen Lagewinkel l_G2 in Weltsystem
        phi_l_g2 = get_angle(self.MCP[0], self.MCP[1], self.F[0], self.F[1])
        self.phi_l_g2 = phi_l_g2
        g_x = self.F[0]+cos(phi_l_g2-self.psi_3)*self.l_9
        g_y = self.F[1]+sin(phi_l_g2-self.psi_3)*self.l_9
        G = [g_x, g_y]
        self.G = G

        # Zweischlag G-H-D
        [h_x, h_y] = get_point(self.D[0], self.D[1],
                               self.l_7, G[0], G[1], self.l_8)
        H = [h_x, h_y]
        self.H = H

    def joint_5_4(self, phi_k):
        """Gelenkfuenfeck 4"""

        pip_x = self.G[0]+cos(self.phi_l_g2-self.psi_3-self.psi_4)*self.l_g3
        pip_y = self.G[1]+sin(self.phi_l_g2-self.psi_3-self.psi_4)*self.l_g3
        PIP = [pip_x, pip_y]
        self.PIP = PIP

        # Bestimmung Abstand PIP-J aus Messung Encoderwinkel phi_K fuer Zweischlag PIP-J-H
        # Winkel gamma zwischen l_G4 und l_11
        gamma = pi-phi_k+self.psi_5
        gamma_d = gamma * (180/pi)
        # Strecke l zwischen PIP und J ueber Kosinussatz
        l_ks = sqrt(self.l_g4**2+self.l_11**2-2 *
                    self.l_g4*self.l_11*cos(gamma))

        # Zweischlag PIP-J-H mit virtueller Laenge l_KS
        [j_x, j_y] = get_point(self.H[0], self.H[1],
                               self.l_10, PIP[0], PIP[1], l_ks)

        J = [j_x, j_y]
        self.J = J

        # ------ Fallunterscheidung notwendig! Lage kann umschlagen! -------------
        # Zweischlag PIP-K-J
        # Bedingung: Winkel gamma zwischen l_G4 und l_11
        if gamma_d < 180:
            [k_x, k_y] = get_point(J[0], J[1], self.l_11,
                                   PIP[0], PIP[1], self.l_g4)
            K = [k_x, k_y]
        else:
            [k_x, k_y] = get_point(
                PIP[0], PIP[1], self.l_g4, J[0], J[1], self.l_11)
            K = [k_x, k_y]
        self.K = K

    def joint_4_5(self):
        """Gelenkviereck 5"""
        phi_t = get_angle(self.PIP[0], self.PIP[1],
                          self.K[0], self.K[1])-self.psi_5
        dip_x = self.PIP[0]+self.l_pm*cos(phi_t)
        dip_y = self.PIP[1]+self.l_pm*sin(phi_t)
        DIP = [dip_x, dip_y]
        self.DIP = DIP

        # Zweischlag DIP-L-J
        [l_x, l_y] = get_point(self.J[0], self.J[1],
                               self.l_12, DIP[0], DIP[1], self.l_g6)
        L = [l_x, l_y]
        self.L = L

        # Position der Fingerspitze
        phi_t = get_angle(DIP[0], DIP[1], L[0], L[1])-self.psi_6
        fs_x = DIP[0]+self.l_pd*cos(phi_t)
        fs_y = DIP[1]+self.l_pd*sin(phi_t)
        FS = [fs_x, fs_y]
        self.FS = FS

    def get_joint_angles(self):
        """
        getJointAngles berechnet die Fingergelenkwinkel aus den bestimmten
        Gelenkpositionen
        Muss nach getKinConfig ausgefuehrt werden
        """

        # Winkel proximales Glied im Weltsystem
        phi_prox_w = get_angle(0, 0, self.PIP[0], self.PIP[1])
        phi_mcp = phi_prox_w*(180/pi)
        self.phi_mcp = phi_mcp
        self.alpha = phi_mcp * (pi/180)

        # Winkel mediales Glied in Weltsystem
        phi_med_w = get_angle(
            self.PIP[0], self.PIP[1], self.DIP[0], self.DIP[1])
        # Winkel PIP Gelenk zwischen PP und PM
        phi_pip = phi_med_w*(180/pi)-phi_mcp
        self.phi_pip = phi_pip
        self.beta = phi_pip * (pi/180)

        # Winkel distales Glied
        phi_dist_w = get_angle(
            self.DIP[0], self.DIP[1], self.FS[0], self.FS[1])
        # Winkel DIP Gelenk zwischen PM und PD
        phi_dip = phi_dist_w*(180/pi)-phi_pip-phi_mcp
        self.phi_dip = phi_dip
        self.gamma = phi_dip * (pi/180)

    def get_stab_angles(self):
        """calculate all angles of the rods"""
        self.phi_1 = get_angle(self.B[0], self.B[1], self.C[0], self.C[1])
        self.phi_2 = get_angle(self.C[0], self.C[1], self.D[0], self.D[1])
        self.phi_3 = get_angle(self.E[0], self.E[1], self.D[0], self.D[1])
        self.phi_4 = get_angle(self.A[0], self.A[1], self.E[0], self.E[1])
        self.phi_6 = get_angle(self.E[0], self.E[1], self.F[0], self.F[1])
        self.phi_7 = get_angle(self.D[0], self.D[1], self.H[0], self.H[1])
        self.phi_8 = get_angle(self.G[0], self.G[1], self.H[0], self.H[1])
        self.phi_10 = get_angle(self.H[0], self.H[1], self.J[0], self.J[1])
        self.phi_11 = get_angle(self.K[0], self.K[1], self.J[0], self.J[1])
        self.phi_12 = get_angle(self.J[0], self.J[1], self.L[0], self.L[1])

    def get_actuation_force(self, f_actor):
        """calculate the force from the actuator"""
        # Winkel zwischen X-Achse und l_s [Check]
        alpha_quer = pi - self.theta - self.phi_1

        # Position Verbindungspunkt Schwinge und Aktor [Check]
        s_x = -self.l_s * cos(alpha_quer)
        s_y = self.l_s * sin(alpha_quer)

        # Winkel des Kraftvektors [Check]
        phi_f = get_angle(self.akt_x, self.akt_y,  s_x, s_y)

        # Komponenten des Kraftvektors in Weltsystem
        f_akt_x = f_actor * cos(phi_f)
        f_akt_y = f_actor * sin(phi_f)

        # Berechnen des Moments um Punkt B, pos. Richtung s. Skizze [Check]
        # Hebelarme für Kraftanteile, pos. delta_x führt zu neg. Moment nach Skizze
        delta_x = -s_x
        delta_y = s_y
        M_B = (f_akt_x * delta_y + f_akt_y * delta_x)
        # %[Nmm]
        self.m_b_nm = M_B/1000

        # Berechnen der Kraft an Spitze von l_1 auf Kinematik
        f_ext = M_B/self.l_1

        # Berechnen der Anteile in X- und Y- Richtung
        self.f_ext_y = -f_ext * cos(self.phi_1)
        self.f_ext_x = f_ext * sin(self.phi_1)

    def get_all_rod_forces(self):
        """calculate all relevant forces of the rods"""
        self.f_1x = -(cos(self.phi_1)*(self.f_ext_y*cos(self.phi_2) -
                                       self.f_ext_x*sin(self.phi_2)))/sin(self.phi_1 - self.phi_2)
        self.f_1y = -(sin(self.phi_1)*(self.f_ext_y*cos(self.phi_2) -
                                       self.f_ext_x*sin(self.phi_2)))/sin(self.phi_1 - self.phi_2)

        self.f_2x = (sin(self.phi_2 - self.phi_7)*sin(self.phi_3 - self.phi_6)*cos(self.phi_4)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_4 - self.phi_6))
        self.f_2y = (sin(self.phi_2 - self.phi_7)*sin(self.phi_3 - self.phi_6)*sin(self.phi_4)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_4 - self.phi_6))

        self.f_3x = -(sin(self.phi_3 - self.phi_4)*sin(self.phi_2 - self.phi_7)*cos(self.phi_6)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                 self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_4 - self.phi_6))
        self.f_3y = -(sin(self.phi_3 - self.phi_4)*sin(self.phi_2 - self.phi_7)*sin(self.phi_6)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                 self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_4 - self.phi_6))

        self.f_4x = -(sin(self.phi_2 - self.phi_3)*sin(self.phi_7 - self.phi_10)*cos(self.phi_8)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                  self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_8 - self.phi_10))
        self.f_4y = -(sin(self.phi_2 - self.phi_3)*sin(self.phi_7 - self.phi_10)*sin(self.phi_8)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                  self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_8 - self.phi_10))

        self.f_5x = (sin(self.phi_2 - self.phi_3)*sin(self.phi_7 - self.phi_8)*sin(self.phi_10 - self.phi_12)*cos(self.phi_11)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                                                self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_8 - self.phi_10)*sin(self.phi_11 - self.phi_12))
        self.f_5y = (sin(self.phi_2 - self.phi_3)*sin(self.phi_7 - self.phi_8)*sin(self.phi_10 - self.phi_12)*sin(self.phi_11)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                                                self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_8 - self.phi_10)*sin(self.phi_11 - self.phi_12))

        self.f_6x = -(sin(self.phi_2 - self.phi_3)*sin(self.phi_7 - self.phi_8)*sin(self.phi_10 - self.phi_11)*cos(self.phi_12)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                                                 self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_8 - self.phi_10)*sin(self.phi_11 - self.phi_12))
        self.f_6y = -(sin(self.phi_2 - self.phi_3)*sin(self.phi_7 - self.phi_8)*sin(self.phi_10 - self.phi_11)*sin(self.phi_12)*(self.f_ext_y*cos(self.phi_1) -
                                                                                                                                 self.f_ext_x*sin(self.phi_1)))/(sin(self.phi_1 - self.phi_2)*sin(self.phi_3 - self.phi_7)*sin(self.phi_8 - self.phi_10)*sin(self.phi_11 - self.phi_12))

    def get_joint_torques(self):
        """get the torques in the three joints"""
        f__11x = self.f_3x
        f__11y = self.f_3y
        f__12x = self.f_4x
        f__12y = self.f_4y
        f__2x = self.f_5x
        f__2y = self.f_5y
        f__3x = self.f_6x
        f__3y = self.f_6y

        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma

        p_11x = self.p_11x
        p_11y = self.p_11y
        p_12x = self.p_12x
        p_12y = self.p_12y
        p_2x = self.p_2x
        p_2y = self.p_2y
        p_3x = self.p_3x
        p_3y = self.p_3y

        # %[Nmm]Berechnen der Gelenkmomente mit ausgew. NE-Gleichungen fuer statischen Zustand
        m_mcp_nmm = f__3y*self.l_c3*cos(alpha + beta + gamma) - f__3x*self.l_c3*sin(alpha + beta + gamma) - (981*self.l_c3*self.m3*cos(alpha + beta + gamma))/100 - f__2x*p_2y*cos(alpha + beta) + f__2y*p_2x*cos(alpha + beta) - f__2x*p_2x*sin(alpha + beta) - f__2y*p_2y*sin(alpha + beta) + f__2y*self.l_c2*cos(alpha + beta) + 2*f__3y*self.l_c2*cos(alpha + beta) - f__2x*self.l_c2*sin(alpha + beta) - 2*f__3x*self.l_c2*sin(alpha + beta) - f__11x*p_11y*cos(alpha) + f__11y*p_11x*cos(alpha) - f__12x*p_12y*cos(alpha) + f__12y*p_12x*cos(alpha) - (981*self.l_c2*self.m2*cos(alpha + beta))/100 - (981*self.l_c2*self.m3*cos(alpha + beta))/50 - \
            f__11x*p_11x*sin(alpha) - f__11y*p_11y*sin(alpha) - f__12x*p_12x*sin(alpha) - f__12y*p_12y*sin(alpha) + 2*f__2y*self.l_c1*cos(alpha) + 2*f__3y*self.l_c1*cos(alpha) + f__11y*self.l_c1*cos(alpha) + f__12y*self.l_c1*cos(alpha) - f__3x*p_3y*cos(alpha + beta + gamma) + f__3y*p_3x*cos(alpha + beta + gamma) - 2*f__2x * \
            self.l_c1*sin(alpha) - 2*f__3x*self.l_c1*sin(alpha) - f__11x*self.l_c1*sin(alpha) - f__12x*self.l_c1*sin(alpha) - f__3x*p_3x*sin(alpha + beta + gamma) - \
            f__3y*p_3y*sin(alpha + beta + gamma) - (981*self.l_c1*self.m1*cos(alpha))/100 - (
                981*self.l_c1*self.m2*cos(alpha))/50 - (981*self.l_c1*self.m3*cos(alpha))/50
        m_pip_nmm = f__3y*self.l_c3*cos(alpha + beta + gamma) - f__3x*self.l_c3*sin(alpha + beta + gamma) - (981*self.l_c3*self.m3*cos(alpha + beta + gamma))/100 - f__2x*p_2y*cos(alpha + beta) + f__2y*p_2x*cos(alpha + beta) - f__2x*p_2x*sin(alpha + beta) - f__2y*p_2y*sin(alpha + beta) + f__2y*self.l_c2*cos(alpha + beta) + 2*f__3y*self.l_c2*cos(
            alpha + beta) - f__2x*self.l_c2*sin(alpha + beta) - 2*f__3x*self.l_c2*sin(alpha + beta) - (981*self.l_c2*self.m2*cos(alpha + beta))/100 - (981*self.l_c2*self.m3*cos(alpha + beta))/50 - f__3x*p_3y*cos(alpha + beta + gamma) + f__3y*p_3x*cos(alpha + beta + gamma) - f__3x*p_3x*sin(alpha + beta + gamma) - f__3y*p_3y*sin(alpha + beta + gamma)
        m_dip_nmm = f__3y*self.l_c3*cos(alpha + beta + gamma) - f__3x*self.l_c3*sin(alpha + beta + gamma) - (981*self.l_c3*self.m3*cos(alpha + beta + gamma))/100 - f__3x*p_3y*cos(
            alpha + beta + gamma) + f__3y*p_3x*cos(alpha + beta + gamma) - f__3x*p_3x*sin(alpha + beta + gamma) - f__3y*p_3y*sin(alpha + beta + gamma)

        # %Umrechnen der Momente in Nm
        self.m_mcp = m_mcp_nmm/1000
        self.m_pip = m_pip_nmm/1000
        self.m_dip = m_dip_nmm/1000


if __name__ == '__main__':
    exo = KinExoParams()

    phi_B = 127.149
    phi_A = 54.724
    phi_K = 73.567

    print(exo(phi_A, phi_B, phi_K, 10))

# %%
