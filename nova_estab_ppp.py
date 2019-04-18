import logging
from Exceptions.HologramError import HologramError
from Hologram.HologramCloud import HologramCloud

hologram = HologramCloud(dict(),network='cellular')
if hologram.network.networkConnected():
    print("Network not yet connected, connecting")
    res = hologram.network.connect()
else:
    print('Network already connected')
