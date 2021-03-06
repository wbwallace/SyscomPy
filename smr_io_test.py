"""generic testing stuff
"""
## this works - at least for the testfile (which should be good enough)
##              compared it to a to_ascii conversion

## http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html

## the resultant numpy array is:
##      array([[ x,  y,  z],
##             [ x,  y,  z],
##             [-3,  0, -5],
##             [-2, -1, -8],
##             [-2, -1, -2]], dtype=int16)

## numpy arrays are indexed array[row, column]
## x data is npData_1[:, 0]
## y data is npData_1[:, 1]
## z data is npData_1[:, 2]


import numpy as np
import struct
import pprint
pp = pprint.pprint


#testfile="c:\\users\\bill\\documents\\SyscomPy\\BMR06003.SMR"
testfile="c:\\users\\bill\\documents\\SyscomPy\\BMR02002.SMR"

# get the data
with open(testfile, 'rb') as f:
    f.seek(256)
    data = f.read()

npData = np.fromstring(data, dtype = np.int16)
npData_1 = npData.reshape((-1, 3))
#np.savetxt(testfile + '.tst', npData_1, fmt = '%s', delimiter = '\t')

#get the header
with open(testfile, 'rb') as f:
    hdr = f.read(256)

# little endian!!!
hdr_format = '< B B B B h I h B h h h 6s b B 5s I B B B B B B B h B B B B B B B h h h h h B B 7s 5s h B B h h h h 6s h B h B h B 9s 5s 5s 5s 15s 3s 3s 3s 9s h h h 6s b B B B 30s h B B B B B B B B B B B B c B 2s B B B c B c B c B c 3s 3s B B B c B c B c B b B 3s 2s'
s = struct.Struct(hdr_format)
raw_hdr = s.unpack(hdr)

##pp(smr_hdr)

hdr_fields = ['file_number', 'block number', 'test_sensor', 'periodic',
              'sum_event', 'nb_samples', 'sampling', 'nb_channel',
              'ch_peak_x', 'ch_peak_y', 'ch_peak_z', 'free1 6 bytes',
              'check_sum', 'sw_revision', 'ss_number', 'sync_offset',
              'sync_second', 'sync_minute', 'sync_hour', 'sync_day',
              'sync_month', 'sync_year', 'sync_ok', 'int_offset(sps)',
              'int_seconds', 'int_minute', 'int_hour', 'int_day', 'int_month',
              'int_year', 'time_valid', 'gnd', 'bat_main', 'bat_backup',
              'bat_module', 'bat_card', 'bat_lsb', 'temperature', 'rec_name',
              's_number', 'filter_freq', 'filter_pole', 'sw_version', 'adc_resol',
              'ch_offset_x', 'ch_offset_y', 'ch_offset_z', 'free2',
              'ch_lsb_mant_x', 'ch_lsb_exp_x', 'ch_lsb_mant_y', 'ch_lsb_exp_y',
              'ch_lsb_mant_z', 'ch_lsb_exp_z', 'free3', 'ch_units_x', 'ch_units_y',
              'ch_units_z', 'free4', 'ch_names_x', 'ch_names_y', 'ch_names_z',
              'free5', 'trigger_x', 'trigger_y', 'trigger_z', 'free6', 'trig_mode',
              'prevent', 'postevent', 'trig_chan', 'comment', 'sync_delay',
              'ac_lost', 'nb_ac_lost', 'day_lost', 'month_lost', 'year_lost',
              'nb_reset', 'day_reset', 'month_reset', 'year_reset', 'errors',
              'dwnld_event', 'warning', 'free7', 'test_sel', 'free8', 'test_anal1',
              'test_anal2', 'test_hardw', 'free9', 'test_clock', 'free10',
              'test_memory', 'free11', 'test_battery', 'free12', 'latitude',
              'longitude', 'mask_anal1', 'mask_anal2', 'mask_hardw', 'free13',
              'mask_clock', 'free14', 'mask_memory', 'free15', 'mask_battery',
              'DSP_settings', 'engg_mode', 'elevation', 'free16']

##smr_hdr = {}
##for i, field in enumerate(hdr_fields):
##    smr_hdr[field] = raw_hdr[i]

smr_hdr = dict(zip(hdr_fields, raw_hdr))

def bcd_to_str(n):
    """ n -> byte"""
    return str(n / 16) + str(n % 16)

smr_hdr['sync_time'] = bcd_to_str(raw_hdr[18]) + ':' + bcd_to_str(raw_hdr[17]) + ':' + str(int(bcd_to_str(raw_hdr[16])) + raw_hdr[15] / 200.)
smr_hdr['sync_date'] = bcd_to_str(raw_hdr[20]) + '/' + bcd_to_str(raw_hdr[19]) + '/' + bcd_to_str(raw_hdr[21])
smr_hdr['trigger_time'] = bcd_to_str(raw_hdr[26]) + ':' + bcd_to_str(raw_hdr[25]) + ':' + str(int(bcd_to_str(raw_hdr[24])) + raw_hdr[23] / 200.)
smr_hdr['trigger_date'] = bcd_to_str(raw_hdr[28]) + '/' + bcd_to_str(raw_hdr[27]) + '/' + bcd_to_str(raw_hdr[29])




#what is this ?? it counts the number of bytes in hdr_format
z = []
l = 0
for i in hdr_format.split(' '):
    z.append((l, i))
    if i in ('B', 'c', 'b'):
        l += 1
    if i in ('h', 'H'):
        l += 2
    if i in ('i', 'I', 'l', 'L'):
        l += 4
    if i.endswith('c') and len(i) > 1:
        l += int(i[:-1])

##pp(z)

