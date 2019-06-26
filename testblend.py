import bge



scene = bge.logic.getCurrentScene()
o1 = scene.objects["a"]
o2 = scene.objects["b"]
if not hasattr(bge.logic, 'video_a'):
    #for o, im, v in [(o1, 'IMin1.png', '/home/student/trub-cv/img/out.avi'), (o2, 'IMin2.png', '/home/student/trub-cv/img/out2.avi')]:
    tex = bge.texture.materialID(o1, 'IMin1.png')
    bge.logic.video_a = bge.texture.Texture(o1, tex)
    bge.logic.video_a.source = bge.texture.VideoFFmpeg('/home/student/trub-cv/img/out.avi')
    bge.logic.video_a.source.scale = True
    bge.logic.video_a.source.play()

if not hasattr(bge.logic, 'video_b'):
    #for o, im, v in [(o1, 'IMin1.png', '/home/student/trub-cv/img/out.avi'), (o2, 'IMin2.png', '/home/student/trub-cv/img/out2.avi')]:
    tex_b = bge.texture.materialID(o2, 'IMin2.png')
    bge.logic.video_b = bge.texture.Texture(o2, tex_b)
    bge.logic.video_b.source = bge.texture.VideoFFmpeg('/home/student/trub-cv/img/out2.avi')
    bge.logic.video_b.source.scale = True
    bge.logic.video_b.source.play()

bge.logic.video_a.refresh(True)
bge.logic.video_b.refresh(True)