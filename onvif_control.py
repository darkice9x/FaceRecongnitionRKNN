""" 
/home/darkice/miniconda3/envs/onvif/lib/python3.11/site-packages/isodate/isodatetime.py의 def parse_datetime(datetimestring)
51번째줄의 아래 문장을
    datestring, timestring = datetimestring.split('T')
아래 문장으로 바꾼다
    date_obj = datetime.strptime(datetimestring, '%a %b %d %H:%M:%S %Y')
    datestring = date_obj.strftime('%Y-%m-%d')
    timestring = date_obj.strftime('%H:%M:%S')

2025-01-25
    onvif-client       0.0.4
    isodate            0.7.2
    onvif2-zeep        0.3.4
    이 패키지에서는 수정 필요없음. 대신 pip install onvif-gui 에서는 안됨.conda install -c conda-forge libstdcxx-ng=12 -y를 설치해야하고
    이렇게 설치된후엔 opencv가 작동을 안함.
"""

try:
    # onvif-client
    from onvif import ONVIFCamera
except:
    # onvif2-zeep, WSDiscovery
    from onvif2 import ONVIFCamera
import time
from datetime import datetime
import socket
import struct
import uuid
import xml.etree.ElementTree as ET
import re
from urllib.parse import urlparse

class OnvifCamera(object):
    def __init__(self,
                camera_ip,
                camera_port,
                camera_user,
                camera_password,
                wsdl_dir
                ) -> None:
        self.camera_ip = camera_ip
        self.camera_port = camera_port
        self.camera_user = camera_user
        self.camera_password = camera_password
        self.wsdl_dir = wsdl_dir

        # ONVIF 카메라 객체 생성
        self.camera = ONVIFCamera(self.camera_ip, self.camera_port, self.camera_user, self.camera_password, self.wsdl_dir )

        # 카메라 프로파일 가져오기
        self.media = self.camera.create_media_service()
        self.profiles = self.media.GetProfiles()

        self.profile = self.profiles[0]

        # Get the video source configuration options
        self.video_source_config = self.media.GetVideoSourceConfigurationOptions({'ProfileToken': self.profile.token})

        # Get video encoder configuration
        self.video_encoder_config = self.media.GetVideoEncoderConfiguration({
            'ConfigurationToken': self.profile.VideoEncoderConfiguration.token
        })

        # Get supported configuration options
        self.options = self.media.GetVideoEncoderConfigurationOptions({
            'ProfileToken': self.profile.token
        })

        # PTZ 서비스 초기화
        self.ptz = self.camera.create_ptz_service()

        # Get PTZ configuration options
        configurations = self.ptz.GetConfigurations()
        ptz_configuration_token = configurations[0].token  # Use the first configuration

        # Get configuration options
        request = self.ptz.create_type('GetConfigurationOptions')
        request.ConfigurationToken = ptz_configuration_token
        self.ptz_configuration_options = self.ptz.GetConfigurationOptions(request)

        #self.get_ptz_status()
        self.Get_Status()

    def Get_Status(self):
        # Get range of pan and tilt
        self.XMAX = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Max
        self.XMIN = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Min
        self.YMAX = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Max
        self.YMIN = self.ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Min
        self.pan = self.ptz.GetStatus({'ProfileToken': self.profile.token}).Position.PanTilt.x
        self.tilt = self.ptz.GetStatus({'ProfileToken': self.profile.token}).Position.PanTilt.y
        self.velocity = self.ptz_configuration_options.Spaces.PanTiltSpeedSpace[0].XRange.Max
        self.zoom = self.ptz.GetStatus({'ProfileToken': self.profile.token}).Position.Zoom.x if self.ptz.GetStatus({'ProfileToken': self.profile.token}).Position.Zoom else None

    def Info(self):
        """
        Operation to request the device information.

        Returns:
            Returns a dictionary with the device information.
        """
        device_info = self.camera.devicemgmt.GetDeviceInformation()
        return {
            'Manufacturer': device_info.Manufacturer,
            'Model': device_info.Model,
            'FirmwareVersion': device_info.FirmwareVersion,
            'SerialNumber': device_info.SerialNumber,
            'HardwareId': device_info.HardwareId
        }

    def Config(self):
        print( self.video_source_config )

    def Profile_Spec(self):
        for profile in self.profiles:
            print(f"Profile: {profile.Name}")
            # Get video encoder configuration
            video_encoder_config = self.media.GetVideoEncoderConfiguration({
                'ConfigurationToken': profile.VideoEncoderConfiguration.token
            })

            # Print current resolution
            print(f"Current Resolution: {video_encoder_config.Resolution.Width}x{video_encoder_config.Resolution.Height}")

            # Print current fps
            print(f"Current Fps: {video_encoder_config.RateControl.FrameRateLimit}")

            # Get supported configuration options
            options = self.media.GetVideoEncoderConfigurationOptions({
                'ProfileToken': profile.token
            })

            print("Supported Resolutions:")
            if options.H264 is not None and hasattr(options.H264, 'ResolutionsAvailable'):
                for res in options.H264.ResolutionsAvailable:
                    # Process each resolution
                    print(f"Width: {res.Width}, Height: {res.Height}")
            else:
                print("H264 options or ResolutionsAvailable is not available.")

    def profile_url(self):
        #resolution = profile.VideoEncoderConfiguration.Resolution
        #fps = profile.VideoEncoderConfiguration.RateControl.FrameRateLimit
        self.stream_setup = {
            'Stream': 'RTP-Unicast',
            'Transport': {
                'Protocol': 'RTSP'
            }
        }
        url_stream = []
        for profile in self.profiles:
            stream_uri = self.media.GetStreamUri({'StreamSetup': self.stream_setup, 'ProfileToken': profile.token})
            url_stream.append(stream_uri['Uri'])
        #self.stream_uri = self.media.GetStreamUri({'StreamSetup': self.stream_setup, 'ProfileToken': self.profile.token})
        return url_stream

    def get_ptz_status(self):
        """
        Operation to request PTZ status.

        Returns:
            Returns a list with the values of Pan, Tilt and Zoom
        """
        request = self.ptz.create_type('GetStatus')
        request.ProfileToken = self.profile.token
        time.sleep(0.1)  # Add a small delay to ensure the request is processed
        ptz_status = self.ptz.GetStatus(request)
        self.pan = ptz_status.Position.PanTilt.x
        self.tilt = ptz_status.Position.PanTilt.y
        self.zoom = ptz_status.Position.Zoom.x if ptz_status.Position.Zoom else None
        self.velocity = self.ptz_configuration_options.Spaces.PanTiltSpeedSpace[0].XRange.Max
        return self.pan, self.tilt, self.zoom, self.velocity

    def absolute_move(self, pan: float, tilt: float, zoom: float, sync: int):
        """
        Operation to move pan, tilt or zoom to an absolute destination.

        Args:
            pan: Pans the device relative to the (0,0) position.
            tilt: Tilts the device relative to the (0,0) position.
            zoom: Zooms the device n steps.

        Returns:
            Return onvif's response
        """
        ppan, ptilt, pzoom, pvelocity = self.get_ptz_status()
        request = self.ptz.create_type('AbsoluteMove')
        request.ProfileToken = self.profile.token
        request.Position = {'PanTilt': {'x': pan, 'y': tilt}, 'Zoom': zoom}
        response = self.ptz.AbsoluteMove(request)
        if sync == 1:
            while True:
                lpan, ltilt, lzoom, lvelocity = self.get_ptz_status()
                #print(f"ppan: {ppan}, lpan: {lpan}, ptilt: {ptilt}, ltilt: {ltilt}, pzoom: {pzoom}, lzoom: {lzoom}")
                if ( ppan != lpan ) or ( ptilt != ltilt ) or ( pzoom != lzoom ):
                    ppan = lpan
                    ptilt = ltilt
                    pzoom = lzoom
                else :
                    break
        return response

    def continuous_move(self, pan: float, tilt: float, zoom: float):
        """
        Operation for continuous Pan/Tilt and Zoom movements.

        Args:
            pan: speed of movement of Pan.
            tilt: speed of movement of Tilt.
            zoom: speed of movement of Zoom.

        Returns:
            Return onvif's response.
        """
        request = self.ptz.create_type('ContinuousMove')
        request.ProfileToken = self.profile.token
        request.Velocity = {'PanTilt': {'x': pan, 'y': tilt}, 'Zoom': zoom}
        response = self.ptz.ContinuousMove(request)
        return response

    def relative_move(self, pan: float, tilt: float, zoom: float, sync: int):
        """
        Operation for Relative Pan/Tilt and Zoom Move.

        Args:
            pan: A positional Translation relative to the pan current position.
            tilt: A positional Translation relative to the tilt current position.
            zoom:

        Returns:
            Return onvif's response
        """
        ppan, ptilt, pzoom, pvelocity = self.get_ptz_status()
        request = self.ptz.create_type('RelativeMove')
        request.ProfileToken = self.profile.token
        request.Translation = {'PanTilt': {'x': pan, 'y': tilt}, 'Zoom': zoom}
        response = self.ptz.RelativeMove(request)
        if sync == 1:
            while True:
                lpan, ltilt, lzoom, lvelocity = self.get_ptz_status()
                #print(f"ppan: {ppan}, lpan: {lpan}, ptilt: {ptilt}, ltilt: {ltilt}, pzoom: {pzoom}, lzoom: {lzoom}")
                if ( ppan != lpan ) or ( ptilt != ltilt ) or ( pzoom != lzoom ):
                    ppan = lpan
                    ptilt = ltilt
                    pzoom = lzoom
                else :
                    break
        return response

    def stop_move(self):
        """
        Operation to stop ongoing pan, tilt and zoom movements of absolute relative and continuous type.

        Returns:
            Return onvif's response
        """
        request = self.ptz.create_type('Stop')
        request.ProfileToken = self.profile.token
        response = self.ptz.Stop(request)
        return response

    def get_preset(self):
        """
        Operation to request all PTZ presets.

        Returns:
            Returns a list of tuples with the presets.
        """
        ptz_get_presets = self.get_preset_complete()

        presets = []
        for ptz_get_preset in ptz_get_presets:
            presets.append(ptz_get_preset.Name)
        return presets

    def get_preset_complete(self):
        """
        Operation to request all PTZ presets.

        Returns:
            Returns the complete presets Onvif.
        """
        request = self.ptz.create_type('GetPresets')
        request.ProfileToken = self.profile.token
        ptz_get_presets = self.ptz.GetPresets(request)
        return ptz_get_presets

    def set_preset(self, preset_name: str):
        """
        The command saves the current device position parameters.
        Args:
            preset_name: Name for preset.

        Returns:
            Return onvif's response.
        """
        presets = self.get_preset_complete()
        request = self.ptz.create_type('SetPreset')
        #print( request )
        request.ProfileToken = self.profile.token
        request.PresetName = preset_name
        #request.PresetToken = '1'

        #for i, preset in enumerate(presets):
        #    if str(presets[i].Name) == preset_name:
        #        return None

        ptz_set_preset = self.ptz.SetPreset(request)
        return ptz_set_preset

    def remove_preset(self, preset_name: str):
        """
        Operation to remove a PTZ preset.

        Args:
            preset_name: Preset name.

        Returns:
            Return onvif's response.
        """
        presets = self.get_preset_complete()
        request = self.ptz.create_type('RemovePreset')
        request.ProfileToken = self.profile.token
        for preset in presets:
            if str(preset.Name) == preset_name:
                print("Remove Preset")
                request.PresetToken = preset.token
                ptz_remove_preset = self.ptz.RemovePreset(request)
                return ptz_remove_preset
        return None

    def go_to_preset(self, preset_position: str):
        """
        Operation to go to a saved preset position.

        Args:
            preset_position: preset name.

        Returns:
            Return onvif's response.
        """
        presets = self.get_preset_complete()
        request = self.ptz.create_type('GotoPreset')
        request.ProfileToken = self.profile.token
        for preset in presets:
            str1 = str(preset.Name)
            if str1 == preset_position:
                request.PresetToken = preset.token
                response = self.ptz.GotoPreset(request)
                return response
        return None

    def set_home_position(self):
        """
        Operation to save current position as the home position.

        Returns:
            Return onvif's response
        """
        request = self.ptz.create_type('SetHomePosition')
        request.ProfileToken = self.profile.token
        response = self.ptz.SetHomePosition(request)
        self.ptz.Stop({'ProfileToken': self.profile.token})
        return response

    def go_home_position(self):
        """
        Operation to move the PTZ device to it's "home" position.

        Returns:
            Return onvif's response
        """
        request = self.ptz.create_type('GotoHomePosition')
        request.ProfileToken = self.profile.token
        response = self.ptz.GotoHomePosition(request)
        return response