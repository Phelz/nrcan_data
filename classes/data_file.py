from datetime import datetime

from scipy.io import loadmat, savemat
import numpy as np

from dataclasses import dataclass

@dataclass
class DataFile:

    file_path: str 

    def __post_init__(self):

        self.data_dic = self.read_file()

        separated_path = self.file_path.split("\\")[-1].replace("dd", "").split("_")
        
        self.link      = separated_path[:2]
        self.date_str  = separated_path[-2]
        self.date_time = datetime.strptime(self.date_str, "%Y%m%d")

        q, r = divmod(int(separated_path[-1].replace(".mat", "")), int(10e5))
        self.frequency = q + r/int(10e5) 


    def read_file(self):

        data_dic = {}
        matrix = loadmat(self.file_path)

        data_dic['antindf']      = matrix['antindf'].ravel()
        data_dic['azimuth']      = matrix['azimuth'].ravel()
        data_dic['clock_oddity'] = matrix['clock_oddity'].ravel()
        data_dic['delspread']    = matrix['delspread'].ravel()
        data_dic['doppler']      = matrix['doppler'].ravel()
        data_dic['dopsindex']    = matrix['dopsindex'].ravel()
        data_dic['dopspread']    = matrix['dopspread'].ravel()
        data_dic['elevation']    = matrix['elevation'].ravel()
        data_dic['hires_az']     = matrix['hires_az']
        data_dic['hires_el']     = matrix['hires_el']
        data_dic['hires_pow']    = matrix['hires_pow']
        data_dic['hires_tof']    = matrix['hires_tof']
        data_dic['ITUdelspr']    = matrix['ITUdelspr']
        data_dic['ITUmps']       = matrix['ITUmps']
        data_dic['mpspread']     = matrix['mpspread'].ravel()
        data_dic['numant']       = matrix['numant'].ravel()
        data_dic['peaktome']     = matrix['peaktomean'].ravel()
        data_dic['sigpow']       = matrix['sigpow'].ravel()
        data_dic['snr']          = matrix['snr'].ravel()
        data_dic['snr_dd']       = matrix['snr_dd'].ravel()
        data_dic['TIME_DELAY']   = matrix['TIME_DELAY']
        data_dic['timeday']      = matrix['timeday'].ravel()
        data_dic['tofazim']      = matrix['tofazim']
        data_dic['tofedaz']      = matrix['tofedaz']
        data_dic['tofedel']      = matrix['tofedel']
        data_dic['tofelev']      = matrix['tofelev']
        data_dic['toflight']     = matrix['toflight']
        data_dic['tofmode']      = matrix['tofmode']


        return data_dic




