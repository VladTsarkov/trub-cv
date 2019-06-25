import bge

cout = bge.logic.getCurrentController()
own = cout.owner
if not hasattr(bge.logic. 'video'):
    tex = bge.texture.materialID(own, 'IMin1.png')
    
    bge.logic.video = bge.texture.Texture(own, tex)
    
    bge.logic.video.source = bge.texture.Videoffmpeg('rtsp://admin:admin@192.168.1.169:554/ch01/2')
    bge.logic.video.source.play()
    
bge.logic.video.refresh(True)