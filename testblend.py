import bge
import cv2 as cv
import datetime
#print(111)

scene = bge.logic.getCurrentScene()
o1 = scene.objects["a"]
o2 = scene.objects["b"]
sens = o1.sensors["Pause"]
#objlist = scene.objects
#print(objlist)
text = scene.objects["Text"]
if not hasattr(bge.logic, 'video_a'):
    #for o, im, v in [(o1, 'IMin1.png', '/home/student/trub-cv/img/out.avi'), (o2, 'IMin2.png', '/home/student/trub-cv/img/out2.avi')]:
    tex = bge.texture.materialID(o1, 'IMin1.png')
    bge.logic.video_a = bge.texture.Texture(o1, tex)
    #bge.logic.video_a.source = bge.texture.VideoFFmpeg("0",0)
    bge.logic.video_a.source = bge.texture.VideoFFmpeg('/home/student/trub-cv/img/out_syn.avi')
    #bge.logic.video_a.source.scale = True
    bge.logic.video_a.source.play()

if not hasattr(bge.logic, 'video_b'):
    #for o, im, v in [(o1, 'IMin1.png', '/home/student/trub-cv/img/out.avi'), (o2, 'IMin2.png', '/home/student/trub-cv/img/out2.avi')]:
    tex_b = bge.texture.materialID(o2, 'IMin2.png')
    bge.logic.video_b = bge.texture.Texture(o2, tex_b)
    #bge.logic.video_b.source = bge.texture.VideoFFmpeg("1",1)
    bge.logic.video_b.source = bge.texture.VideoFFmpeg('/home/student/trub-cv/img/out2_syn.avi')
    #bge.logic.video_b.source.scale = True
    bge.logic.video_b.source.flip = False
    bge.logic.video_b.source.play()

#print(type(bge.logic.video_a.source))
print(str(datetime.datetime.now().time()))
text.text = str(datetime.datetime.now().time())
bge.logic.video_a.refresh(True)
bge.logic.video_b.refresh(True)

es = sens.events[0]
if es[1]==1:
    keyCode = es[0]
    print("TUT", keyCode)
    if keyCode == 32:
        print("what")
        bge.logic.video_a.source.pause()
        bge.logic.video_b.source.pause()
    if keyCode == 98:
        bge.logic.video_a.source.play()
        bge.logic.video_b.source.play()
    if keyCode == 114:
        bge.logic.video_a.source.stop()
        bge.logic.video_b.source.stop()
        bge.logic.video_a.source.play()
        bge.logic.video_b.source.play()