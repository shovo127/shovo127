import bpy
import math
import os
from mathutils import Vector

OUT=os.environ.get("PROFILE_RENDER_DIR","/tmp/profile-render")
os.makedirs(OUT,exist_ok=True)
W,H=1200,300
FRAMES=20

def mat(name,color,metal=0.0,rough=.35,emission=None):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value=(*color,1)
    p.inputs["Metallic"].default_value=metal
    p.inputs["Roughness"].default_value=rough
    if emission:
        emission_input = p.inputs.get("Emission Color") or p.inputs.get("Emission")
        if emission_input: emission_input.default_value=(*emission,1)
        if p.inputs.get("Emission Strength"): p.inputs["Emission Strength"].default_value=.32
    # Fine-scale surface variation keeps machined metal from looking like flat plastic.
    nodes=m.node_tree.nodes; links=m.node_tree.links
    noise=nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value=145; noise.inputs["Detail"].default_value=2
    bump=nodes.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=.075; bump.inputs["Distance"].default_value=.012
    links.new(noise.outputs["Fac"],bump.inputs["Height"]); links.new(bump.outputs["Normal"],p.inputs["Normal"])
    return m

STEEL=mat("Brushed titanium",(0.36,.43,.48),.88,.24)
DARK=mat("Graphite ceramic",(.025,.042,.052),.48,.27)
BLACK=mat("Rubber and carbon",(.012,.018,.021),.08,.62)
GLASS=mat("Optical glass",(.018,.08,.095),.65,.12,(.015,.12,.14))
GOLD=mat("Machined brass",(.62,.39,.14),.82,.23)
WHITE=mat("Ceramic white",(.72,.77,.78),.18,.26)
TEAL=mat("Signal teal",(.025,.32,.29),.45,.23,(.015,.20,.17))
FLOOR=mat("Studio floor",(.012,.019,.025),.12,.42)

def assign(obj,material):
    obj.data.materials.append(material); return obj

def bevel(obj,width=.06,segments=3):
    if obj.type=="MESH":
        mod=obj.modifiers.new("Machined edge radii","BEVEL"); mod.width=width; mod.segments=segments
        obj.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    return obj

def cube(name,loc,scale,material,bev=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    assign(o,material)
    if bev: bevel(o,bev)
    return o

def cyl(name,loc,radius,depth,material,vertices=96,bev=.025):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    o=bpy.context.object; o.name=name; assign(o,material)
    if bev: bevel(o,bev)
    return o

def torus(name,loc,major,minor,material,rotation=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=96,minor_segments=16,location=loc)
    o=bpy.context.object; o.name=name; assign(o,material)
    if rotation: o.rotation_euler=rotation
    return o

def sphere(name,loc,radius,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=radius,location=loc)
    o=bpy.context.object; o.name=name; assign(o,material)
    bpy.ops.object.shade_smooth(); return o

def rod(name,a,b,r,material):
    mid=(Vector(a)+Vector(b))/2; direction=Vector(b)-Vector(a)
    o=cyl(name,mid,r,direction.length,material)
    o.rotation_euler=direction.to_track_quat("Z","Y").to_euler()
    return o

def text_obj(body,loc,size,material):
    bpy.ops.object.text_add(location=loc,rotation=(math.radians(90),0,0))
    o=bpy.context.object; o.data.body=body; o.data.size=size; o.data.extrude=.001
    assign(o,material); return o

def hero_turbo():
    # A restrained, machined turbocharger assembly as the profile's hero object.
    torus("Turbo compressor housing",(2,0,0),.93,.24,STEEL,(math.pi/2,0,0))
    torus("Machined housing lip",(2,-.23,0),.92,.055,GOLD,(math.pi/2,0,0))
    cyl("Compressor inlet",(2,-.24,0),.68,.12,DARK,bev=.035).rotation_euler[0]=math.pi/2
    cyl("Compressor hub",(2,-.34,0),.19,.12,STEEL,bev=.025).rotation_euler[0]=math.pi/2
    for i in range(11):
        a=2*math.pi*i/11
        x=2+.48*math.cos(a); z=.48*math.sin(a)
        rod("Compressor impeller blade",(2,-.39,0),(x,-.39,z),.045,WHITE)
    cyl("Turbine shaft",(2,.34,0),.22,.95,STEEL,bev=.025).rotation_euler[0]=math.pi/2
    torus("Rear turbine flange",(2,.82,0),.62,.1,STEEL,(math.pi/2,0,0))
    for i in range(8):
        a=2*math.pi*i/8
        sphere("Flange bolt",(2+.78*math.cos(a),.82,.78*math.sin(a)),.065,GOLD)

def piston():
    cyl("Piston crown",(2.1,0,.2),.88,.28,STEEL)
    for z in (.02,.12,.22):
        torus("Piston compression ring",(2.1,0,z),.86,.035,GOLD)
    cyl("Piston skirt",(2.1,0,-.45),.77,.9,DARK)
    cyl("Wrist pin",(2.1,-.79,-.55),.22,.18,STEEL,bev=.02).rotation_euler[0]=math.pi/2
    rod("Forged connecting rod",(2.1,0,-.75),(2.1,.05,-1.75),.19,STEEL)
    torus("Big end bearing",(2.1,.05,-1.75),.31,.11,STEEL)
    for x in (1.85,2.35): cyl("Fastener",(x,.05,-1.75),.055,.12,GOLD,bev=.01)

def chip():
    cube("Processor substrate",(2,0,0),(2.1,1.6,.22),DARK,.12)
    cube("Silicon package",(2,-.02,.2),(1.25,.95,.28),STEEL,.08)
    cube("Glass die",(2,-.02,.37),(.95,.68,.055),GLASS,.025)
    for x in range(7):
        for y in range(5):
            cube("Gold contact",(1.22+x*.26,-.61+y*.28,-.16),(.09,.09,.09),GOLD,.018)
    for x in (-.7,-.35,0,.35,.7):
        cube("Circuit trace",(2+x,-.02,.405),(.025,.55,.012),TEAL,.005)

def phone():
    cube("Unibody phone",(2,0,0),(1.25,.13,2.25),STEEL,.16)
    cube("OLED display",(2,-.075,.02),(1.12,.018,2.08),GLASS,.1)
    cube("Camera island",(2.38,-.095,.82),(.34,.035,.44),DARK,.07)
    for x,z in ((2.3,.9),(2.46,.9),(2.3,.74)):
        torus("Camera lens",(x,-.12,z),.065,.018,STEEL,(math.pi/2,0,0))
    cube("Speaker slot",(2,-.12,-.96),(.22,.018,.025),BLACK,.01)

def book():
    cube("Leather notebook",(1.95,0,0),(1.7,.38,2.05),DARK,.09)
    cube("Ivory page block",(1.95,-.205,0),(1.58,.045,1.94),WHITE,.018)
    cube("Leather cover",(1.95,-.245,0),(1.72,.055,2.08),GOLD,.04)
    rod("Precision pen",(3.15,-.1,-.72),(3.15,-.1,.78),.045,STEEL)
    sphere("Pen finial",(3.15,-.1,.8),.06,GOLD)

def laptop():
    cube("Machined laptop base",(2,-.05,-.72),(2.5,1.65,.14),STEEL,.07)
    cube("Keyboard deck",(2,-.08,-.635),(2.32,1.43,.025),DARK,.03)
    for row in range(4):
        for col in range(13):
            cube("Keycap",(.95+col*.175,.35-row*.22,-.61),(.13,.14,.025),STEEL,.018)
    cube("Display housing",(2,.62,.35),(2.5,.13,1.85),STEEL,.09)
    cube("Display glass",(2,.545,.35),(2.34,.018,1.68),GLASS,.035)
    for j in range(5):
        cube("Display data line",(2,.53,.78-j*.23),(1.45-j*.14,.012,.018),TEAL,.006)

def monitor_dashboard():
    cube("Monitor stand",(2,0,-.95),(.18,.25,.7),STEEL,.04)
    cube("Monitor base",(2,-.05,-1.27),(1.2,.62,.08),DARK,.04)
    cube("Monitor chassis",(2,0,.0),(3.1,.17,1.95),STEEL,.09)
    cube("Dashboard glass",(2,-.095,.0),(2.91,.018,1.76),GLASS,.035)
    for j,h in enumerate((.38,.7,.52,.95,.82,.62,.98)):
        x=.95+j*.34
        cube("Analytics column",(x,-.12,-.53+h/2),(.16,.025,h),TEAL,.025)
    for j in range(4):
        cube("Metric panel",(.95+j*.66,-.12,.62),(.48,.025,.22),DARK,.025)
    torus("Metric ring",(2.9,-.13,.58),.2,.035,GOLD,(math.pi/2,0,0))

def trophy():
    cyl("Award plinth",(2,0,-1.05),.92,.2,DARK)
    cyl("Engraved brass ring",(2,0,-.91),.86,.045,GOLD)
    cyl("Trophy stem",(2,0,-.42),.14,.9,STEEL)
    torus("Trophy collar",(2,0,-.05),.28,.055,GOLD)
    # A machined cup assembled from a bowl, flared rim and handles.
    cyl("Trophy bowl",(2,0,.38),.52,.72,GOLD)
    torus("Trophy lip",(2,0,.76),.53,.055,STEEL)
    torus("Left handle",(1.42,0,.42),.3,.065,GOLD,(0,math.pi/2,0))
    torus("Right handle",(2.58,0,.42),.3,.065,GOLD,(0,math.pi/2,0))
    sphere("Award crest",(2,-.29,.42),.13,WHITE)

def city():
    for i,(x,y,h,w) in enumerate(((.3,0,1.6,.65),(1.15,.2,2.5,.72),(2.05,0,1.9,.72),(2.9,.1,3.1,.75),(3.85,0,1.35,.62),(4.6,.15,2.1,.68))):
        cube("Architectural tower",(x,y,h/2-1),(w,w,h),STEEL if i%2 else DARK,.035)
        for z in range(1,int(h*2)):
            for side in (-1,1):
                cube("Window glazing",(x+side*(w/2+.006),y-.03,-1+z*.42),(.018,.28,.16),GLASS,.008)
    cube("City plinth",(2.4,.15,-1.18),(5.4,1.5,.18),DARK,.06)
    for x in (.4,1.3,2.2,3.1,4.0):
        cube("Street light",(x,-.72,-.5),(.025,.025,1.1),GOLD,.01)
        sphere("Street lamp",(x,-.72,.08),.055,WHITE)

def keyboard():
    cube("Desk surface",(2,.3,-1.08),(5.5,2.4,.16),DARK,.08)
    cube("Monitor body",(2,.75,.25),(2.65,.16,1.8),STEEL,.08)
    cube("Monitor glass",(2,.655,.25),(2.48,.02,1.62),GLASS,.04)
    cube("Keyboard body",(2,-.5,-.82),(2.4,.72,.12),BLACK,.07)
    for row in range(4):
        for col in range(14):
            cube("Keyboard key",(1.0+col*.15,-.26-row*.15,-.745),(.12,.11,.045),STEEL,.015)
    torus("Mouse",(3.65,-.45,-.75),.19,.08,STEEL,(math.pi/2,0,0))
    rod("Desk lamp arm",(4,.3,-1),(4.35,.3,.15),.035,STEEL)
    torus("Desk lamp shade",(4.35,.3,.2),.24,.055,GOLD)

def wheel():
    torus("Performance tyre",(2,0,0),.94,.25,BLACK,(math.pi/2,0,0))
    torus("Sidewall detail",(2,-.19,0),.94,.035,STEEL,(math.pi/2,0,0))
    cyl("Forged alloy rim",(2,0,0),.72,.22,STEEL)
    cyl("Hub recess",(2,-.13,0),.43,.04,DARK)
    cyl("Centre cap",(2,-.17,0),.18,.05,GOLD)
    for i in range(10):
        a=2*math.pi*i/10
        x=2+.55*math.cos(a); z=.55*math.sin(a)
        rod("Forged spoke",(2,-.16,0),(x,-.16,z),.055,WHITE)
        cyl("Wheel bolt",(x,-.19,z),.035,.035,GOLD,bev=.008)

def connector():
    cyl("Industrial connector shell",(2,0,0),.56,1.25,STEEL,bev=.08).rotation_euler[0]=math.pi/2
    torus("Connector locking ring",(2,-.42,0),.56,.08,GOLD,(math.pi/2,0,0))
    cyl("Connector face",(2,-.66,0),.43,.08,DARK,bev=.02).rotation_euler[0]=math.pi/2
    for i in range(8):
        a=2*math.pi*i/8
        sphere("Contact pin",(2+.29*math.cos(a),-.72,.29*math.sin(a)),.055,GOLD)
    rod("Cable",(2,.55,0),(3.7,1.0,0),.18,BLACK)
    torus("Cable strain relief",(2.7,.78,0),.2,.04,STEEL,(0,math.pi/2,0))

SCENES=[
 ("00-hero",hero_turbo),
 ("01-about",piston),
 ("02-engineering-focus",chip),
 ("03-featured-work",laptop),
 ("04-technology",phone),
 ("05-command-center",monitor_dashboard),
 ("06-achievements",trophy),
 ("07-contribution-city",city),
 ("09-coding-habits",keyboard),
 ("10-learning-loop",book),
 ("11-beyond-code",wheel),
 ("12-connect",connector),
]

def aim(obj,point):
    obj.rotation_euler=(Vector(point)-obj.location).to_track_quat("-Z","Y").to_euler()

for slug,builder in SCENES:
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    before=set(bpy.data.objects)
    root=bpy.data.objects.new("Animated product assembly",None); bpy.context.collection.objects.link(root)
    bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-1.45))
    floor=bpy.context.object; floor.name="Matte studio cyclorama"; assign(floor,FLOOR)
    builder()
    for obj in set(bpy.data.objects)-before-{root,floor}:
        if obj.type in {"MESH","FONT","CURVE"}:
            obj.parent=root
    # Product photography lighting: broad key, cool fill and warm rim.
    bpy.ops.object.camera_add(location=(2.1,-13.5,3.1))
    camera=bpy.context.object; camera.data.type="ORTHO"; camera.data.ortho_scale=12.2; aim(camera,(2.0,0,0))
    scene=bpy.context.scene; scene.camera=camera
    for name,loc,power,size,color in (
      ("Large softbox key",(-1,-5,7),1500,7,(.78,.88,1)),
      ("Cool edge strip",(6,2,4),1900,5,(.38,.72,.82)),
      ("Warm rim",(0,3,2),1100,4,(1,.69,.42)),
      ("Front fill",(4,-6,1),500,5,(.72,.82,1))):
        bpy.ops.object.light_add(type="AREA",location=loc)
        light=bpy.context.object; light.name=name; light.data.energy=power; light.data.shape="DISK"; light.data.size=size; light.data.color=color; aim(light,(2,0,0))
    scene.render.engine="CYCLES"; scene.cycles.samples=20
    scene.cycles.use_denoising=True
    scene.render.resolution_x=W; scene.render.resolution_y=H; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"; scene.render.film_transparent=False
    scene.world.color=(.012,.018,.025)
    if "AgX" in scene.view_settings.bl_rna.properties["view_transform"].enum_items:
        scene.view_settings.view_transform="AgX"
    else:
        scene.view_settings.view_transform="Filmic"
    scene.render.image_settings.color_mode="RGB"
    scene.frame_start=1; scene.frame_end=FRAMES
    # A restrained product turn, not a fast decorative loop.
    root.rotation_euler[2]=math.radians(-2.2); root.keyframe_insert(data_path="rotation_euler",frame=1)
    root.rotation_euler[2]=math.radians(2.2); root.keyframe_insert(data_path="rotation_euler",frame=FRAMES)
    if root.animation_data and root.animation_data.action:
        for fc in root.animation_data.action.fcurves:
            for key in fc.keyframe_points: key.interpolation="BEZIER"
    scene.render.filepath=os.path.join(OUT,slug+"_")
    for frame in range(1,FRAMES+1):
        scene.frame_set(frame)
        scene.render.filepath=os.path.join(OUT,slug+"_%03d.png"%frame)
        bpy.ops.render.render(write_still=True)
    print("RENDERED_PROFILE_SCENE",slug)
