"""Blender (bpy) scene: Christmas helicopter towing the banner 'JÁ AGENDOU SEU HORÁRIO?'.
Renders an RGBA PNG sequence (1080x1920, 30 fps, transparent background) to composite over the video.
usage: python3 heli_blender.py OUTDIR [frame ...]   (no frames = full animation)"""
import sys, math, os
import bpy

OUT = sys.argv[1]
ONLY = [int(f) for f in sys.argv[2:]]
D = os.path.dirname(os.path.abspath(__file__))
FPS, NF = 30, 303
R = math.radians

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.device = 'CPU'
sc.cycles.samples = int(os.environ.get('SAMPLES', 40))
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1080, 1920, 100
sc.render.fps = FPS
sc.frame_start, sc.frame_end = 1, NF
sc.render.film_transparent = True
sc.render.use_motion_blur = True
sc.render.motion_blur_shutter = 0.5
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'
sc.view_settings.look = 'Medium High Contrast'
# render only the sky band where the helicopter flies
sc.render.use_border = True
sc.render.use_crop_to_border = False
sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
sc.render.border_min_y, sc.render.border_max_y = float(os.environ.get('BMIN', 0.42)), float(os.environ.get('BMAX', 0.95))

# ---------- world + light (overcast day) ----------
world = bpy.data.worlds.new('W'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.70, 0.76, 0.86, 1); bg.inputs[1].default_value = 0.9
sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN')); sc.collection.objects.link(sun)
sun.data.energy = 4.0; sun.data.angle = R(12); sun.rotation_euler = (R(35), R(-25), R(20))
fill = bpy.data.objects.new('Fill', bpy.data.lights.new('Fill', 'SUN')); sc.collection.objects.link(fill)
fill.data.energy = 0.8; fill.data.angle = R(40); fill.rotation_euler = (R(160), 0, 0)   # bounce light from the street onto the belly

# ---------- camera: low angle from the street ----------
cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam')); sc.collection.objects.link(cam); sc.camera = cam
cam.data.sensor_fit = 'VERTICAL'; cam.data.sensor_height = 36; cam.data.lens = 30
cam.location = (0, 0, 0); cam.rotation_euler = (R(90 + 20), 0, 0)


def mat(name, color, metal=0.0, rough=0.35, coat=0.0, emit=None, estr=0.0, alpha=1.0, tex=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rough
    p.inputs['Coat Weight'].default_value = coat
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = estr
    if tex:
        t = m.node_tree.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(tex)
        m.node_tree.links.new(t.outputs['Color'], p.inputs['Base Color'])
    return m


RED = mat('red', (0.62, 0.02, 0.04), metal=0.15, rough=0.22, coat=1.0)
WHITE = mat('white', (0.85, 0.85, 0.83), rough=0.3, coat=0.6)
GLASS = mat('glass', (0.02, 0.03, 0.05), metal=0.2, rough=0.05, coat=1.0)
DARK = mat('dark', (0.04, 0.04, 0.045), metal=0.6, rough=0.35)
METAL = mat('metal', (0.6, 0.6, 0.62), metal=1.0, rough=0.25)
GOLD = mat('gold', (0.85, 0.6, 0.22), metal=1.0, rough=0.2)
GREEN = mat('green', (0.02, 0.18, 0.06), rough=0.55)
ROPE = mat('rope', (0.35, 0.3, 0.25), rough=0.8)
BANNER = mat('banner', (1, 1, 1), rough=0.7, tex=os.path.join(D, 'faixa.png'))
BULBS = [mat('b_r', (1, 0.1, 0.1), emit=(1, 0.08, 0.05), estr=18), mat('b_g', (0.1, 1, 0.2), emit=(0.1, 1, 0.25), estr=14),
         mat('b_y', (1, 0.8, 0.3), emit=(1, 0.75, 0.3), estr=18)]

root = bpy.data.objects.new('HELI', None); sc.collection.objects.link(root); root.scale = (0.72, 0.72, 0.72)


def add(op, m, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), parent=None, smooth=True, **kw):
    getattr(bpy.ops.mesh, op)(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object; o.scale = scale; o.data.materials.append(m)
    if smooth:
        for poly in o.data.polygons: poly.use_smooth = True
    o.parent = parent or root
    return o


# fuselage (nose points to -X, the flight direction)
body = add('primitive_uv_sphere_add', RED, (0, 0, 0), scale=(2.1, 1.05, 1.05), segments=48, ring_count=24)
add('primitive_uv_sphere_add', GLASS, (-1.15, 0, 0.18), scale=(1.15, 0.92, 0.82), segments=48, ring_count=24)
add('primitive_cylinder_add', WHITE, (0.15, 0, -0.78), rot=(0, R(90), 0), scale=(0.4, 0.8, 1.45), vertices=48)   # white belly band
# tail
add('primitive_cone_add', WHITE, (3.2, 0, 0.25), rot=(0, R(90), 0), radius1=0.42, radius2=0.14, depth=4.2, vertices=32)
add('primitive_cube_add', RED, (5.1, 0, 0.95), rot=(0, R(-25), 0), scale=(0.32, 0.03, 0.85), smooth=False)
add('primitive_cube_add', WHITE, (4.6, 0, 0.28), scale=(0.22, 0.75, 0.025), smooth=False)
trot = bpy.data.objects.new('TR', None); sc.collection.objects.link(trot); trot.parent = root; trot.location = (5.2, -0.12, 0.7)
for a in (0, 90):
    add('primitive_cube_add', DARK, (0, 0, 0), rot=(0, R(a), 0), scale=(0.07, 0.02, 0.55), parent=trot, smooth=False)
# mast + main rotor
add('primitive_cylinder_add', DARK, (0.05, 0, 1.15), scale=(0.12, 0.12, 0.3), vertices=24)
mrot = bpy.data.objects.new('MR', None); sc.collection.objects.link(mrot); mrot.parent = root; mrot.location = (0.05, 0, 1.45)
add('primitive_cylinder_add', METAL, (0, 0, 0), scale=(0.28, 0.28, 0.08), parent=mrot, vertices=24)
for a in (0, 90, 180, 270):
    b = add('primitive_cube_add', DARK, (0, 0, 0), rot=(0, 0, R(a)), scale=(2.9, 0.16, 0.025), parent=mrot, smooth=False)
    b.location = (2.9 * math.cos(R(a)), 2.9 * math.sin(R(a)), 0)
# skids + Christmas lights along them
for yv in (-0.85, 0.85):
    add('primitive_cylinder_add', METAL, (-0.1, yv, -1.45), rot=(0, R(90), 0), scale=(0.06, 0.06, 2.0), vertices=16)
    for xv in (-0.9, 0.9):
        add('primitive_cylinder_add', METAL, (xv, yv * 0.85, -1.15), rot=(R(-20 if yv < 0 else 20), 0, 0), scale=(0.05, 0.05, 0.38), vertices=12)
    for i in range(13):
        add('primitive_uv_sphere_add', BULBS[i % 3], (-1.9 + i * 0.3, yv, -1.53), scale=(0.075, 0.075, 0.075), segments=12, ring_count=8)
# wreath on the door (camera side is -Y)
add('primitive_torus_add', GREEN, (0.35, -1.0, -0.05), rot=(R(90), 0, 0), major_radius=0.42, minor_radius=0.12, major_segments=40, minor_segments=12)
for k in range(8):
    a = R(45 * k + 10)
    add('primitive_uv_sphere_add', BULBS[0] if k % 2 else GOLD, (0.35 + 0.42 * math.cos(a), -1.12, -0.05 + 0.42 * math.sin(a)), scale=(0.07, 0.07, 0.07), segments=12, ring_count=8)
add('primitive_cube_add', RED, (0.35, -1.13, -0.5), scale=(0.16, 0.03, 0.1), smooth=False)    # bow
# banner: pole, ropes and the waving cloth
BX0, BW, BH, BTOP = 6.1, 16.0, 2.92, -0.2
add('primitive_cylinder_add', METAL, (BX0, 0, BTOP - BH / 2), scale=(0.05, 0.05, BH / 2 + 0.15), vertices=12)


def rope(p1, p2):
    import mathutils
    v = mathutils.Vector(p2) - mathutils.Vector(p1)
    o = add('primitive_cylinder_add', ROPE, tuple((mathutils.Vector(p1) + mathutils.Vector(p2)) / 2), scale=(0.025, 0.025, v.length / 2), vertices=8)
    o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = v.to_track_quat('Z', 'Y')


rope((5.1, 0, 0.2), (BX0, 0, BTOP + 0.1)); rope((5.1, 0, 0.2), (BX0, 0, BTOP - BH - 0.1))
bpy.ops.mesh.primitive_plane_add(size=1, location=(BX0 + BW / 2, 0, BTOP - BH / 2), rotation=(R(90), 0, 0))
ban = bpy.context.active_object; ban.scale = (BW, BH, 1); ban.parent = root; ban.data.materials.append(BANNER)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.subdivide(number_cuts=60); bpy.ops.object.mode_set(mode='OBJECT')
vg = ban.vertex_groups.new(name='flutter')
for v in ban.data.vertices:
    vg.add([v.index], min(1.0, (v.co.x + 0.5) ** 1.3 * 1.6), 'REPLACE')     # front edge fixed, tail end flutters most
for poly in ban.data.polygons: poly.use_smooth = True
w = ban.modifiers.new('wave', 'WAVE'); w.use_x, w.use_y = True, False
w.height, w.width, w.narrowness, w.speed = 0.06, 0.35, 1.2, 0.012
w.vertex_group = 'flutter'; w.start_position_x = -0.5

# ---------- flight path ----------
YD, ZH = 28.4, 18.8          # 34 m away, ~33 deg above the horizon


def key(f, x, pitch, bank):
    root.location = (x, YD, ZH + 0.25 * math.sin(f / 13.0)); root.keyframe_insert('location', frame=f)
    root.rotation_euler = (R(bank), R(pitch), R(-4)); root.keyframe_insert('rotation_euler', frame=f)


key(1, 30, 9, 0); key(96, -5.6, 3, 1.5); key(204, -7.8, 2, -1.0); key(303, -32, 10, 0)
for fc in root.animation_data.action.fcurves if hasattr(root.animation_data.action, 'fcurves') else []:
    for k in fc.keyframe_points: k.interpolation = 'BEZIER'; k.handle_left_type = k.handle_right_type = 'AUTO'
# rotors spin (motion blur turns them into a disc, like a real camera)
for f in range(1, NF + 1):
    mrot.rotation_euler = (0, 0, R(-37 * f)); mrot.keyframe_insert('rotation_euler', frame=f)
    trot.rotation_euler = (0, R(61 * f), 0); trot.keyframe_insert('rotation_euler', frame=f)

frames = ONLY or range(1, NF + 1)
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = os.path.join(OUT, f'h_{f:04d}.png')
    bpy.ops.render.render(write_still=True)
print('ok')
