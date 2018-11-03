from mqtt_location import *

sunlight_lamp_set =     "/power/sunlight/set"
sunlight_lamp_query =   "/power/sunlight/query"
sunlight_lamp_status =  "/power/sunlight/status"

spotify_play =          lambda location: "/media/spotify/{}/play".format(location.name)
spotify_pause =         lambda location: "/media/spotify/{}/pause".format(location.name)
spotify_skip =          lambda location: "/media/spotify/{}/skip".format(location.name)
spotify_open_url =      lambda location: "/media/spotify/{}/open-url".format(location.name)
spotify_query_volume =  lambda location: "/media/spotify/{}/query-volume".format(location.name)
spotify_played =        lambda location: "/media/spotify/{}/played".format(location.name)
spotify_paused =        lambda location: "/media/spotify/{}/paused".format(location.name)
spotify_metadata =      lambda location: "/media/spotify/{}/metadata".format(location.name)
spotify_volume_status = lambda location: "/media/spotify/{}/volume-status".format(location.name)

wheel_spin =            "/wheel/spin"
wheel_spun =            "/wheel/spun"

