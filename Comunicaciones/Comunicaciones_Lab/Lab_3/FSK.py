

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
from PyQt4 import Qt
import os

class fsk(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transmisor FSK")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transmisor FSK")
        qtgui.util.check_set_qt_gui_path()
        
        if sys.platform.startswith('linux'):
            try:
                self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
            except:
                pass
        
        self.setFixedSize(1280, 768) # Default window size, can be adjusted or set via window_size parameter

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 80e4

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, # size
            samp_rate, # samp_rate
            "", # name
            1 # number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)
        
        if not False:
            self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["Signal 1", "Signal 2", "Signal 3", "Signal 4", "Signal 5", "Signal 6", "Signal 7", "Signal 8", "Signal 9", "Signal 10"]
        colors = ["blue", "red", "green", "black", "cyan", "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        widths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if i < len(labels):
                self.qtgui_time_sink_x_0.set_curve_label(i, labels[i])
                self.qtgui_time_sink_x_0.set_color_curve(i, colors[i])
                self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
                self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
                self.qtgui_time_sink_x_0.set_marker_style(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
        
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, # fftsize
            firdes.WIN_BLACKMAN_hARRIS, # wintype
            0, # fc
            samp_rate, # bw
            "", # name
            1 # number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label("Relative Gain", "dB")
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_show_options(False)
        self.qtgui_freq_sink_x_0.set_fft_attribute_mode(qtgui.qtgui_sink_tool_bar.FIXED_CONTINUOUS)
        self.qtgui_freq_sink_x_0.set_show_peak_instr(False)
        self.qtgui_freq_sink_x_0.set_show_reset_button(False)
        self.qtgui_freq_sink_x_0.set_x_axis_units("Hz")
        self.qtgui_freq_sink_x_0.set_y_axis_units("dB")
        self.qtgui_freq_sink_x_0.set_is_open(True)
        
        if not False:
            self.qtgui_freq_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "", "", "", "", "", ""]
        colors = ["blue", "red", "green", "black", "cyan", "magenta", "yellow", "dark red", "dark green", "dark blue"]
        widths = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if i < len(labels):
                self.qtgui_freq_sink_x_0.set_curve_label(i, labels[i])
                self.qtgui_freq_sink_x_0.set_color_curve(i, colors[i])
                self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
                self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
        
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_multiply_xx_1 = blocks.multiply_xx(gr.sizeof_float*1, 2)
        self.blocks_multiply_xx_0 = blocks.multiply_xx(gr.sizeof_float*1, 2)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_xx_0 = blocks.add_ff(1)
        self.analog_sig_source_x_2 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 100000, 1, 0)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 300000, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_b(samp_rate, analog.GR_SQR_WAVE, 10000, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_not_xx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_uchar_to_float_0, 0))    
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_1, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_not_xx_0, 0), (self.blocks_uchar_to_float_1, 0))    
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_uchar_to_float_1, 0), (self.blocks_multiply_xx_1, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.analog_sig_source_x_2.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)


def main(top_block_cls=fsk, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()