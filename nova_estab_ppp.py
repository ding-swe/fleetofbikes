import logging
from Exceptions.HologramError import HologramError
from Hologram.HologramCloud import HologramCloud

hologram = HologramCloud(dict(),network='cellular')
if hologram._networkManager.networkConnected():
    print('Network already connected')
else:
    print("Network not yet connected, connecting")
    res = hologram.network.connect()
