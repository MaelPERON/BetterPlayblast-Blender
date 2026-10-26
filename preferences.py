"""BetterPlayblast Addon Preferences"""

import bpy


class BP_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__ or "BetterPlayblast-Blender"

    # ── Output ─────────────────────────────────────────────────────────────────
    output_folder_mode: bpy.props.EnumProperty(  # type: ignore
        name="Output Folder",
        items=[
            ("VIDEOS",  "Videos Folder",  "Save in 'videos' folder (sibling of workVersions)"),
            ("PROJECT", "Project Folder", "Save next to the .blend file"),
            ("SYSTEM",  "System Folder",  "Save in a custom system folder"),
        ],
        default="VIDEOS"
    )
    project_subfolder_enabled: bpy.props.BoolProperty(name="Use Subfolder", default=False)  # type: ignore
    project_subfolder_name:    bpy.props.StringProperty(name="Subfolder Name", default="videos")  # type: ignore
    system_folder_path:        bpy.props.StringProperty(name="Folder Path", default="", subtype='DIR_PATH')  # type: ignore

    playblast_name_mode: bpy.props.EnumProperty(  # type: ignore
        name="Playblast Name",
        items=[
            ("FILENAME", "Same as Filename", "Use .blend filename (strips .0001 suffix)"),
            ("CUSTOM",   "Custom Name",       "Use a custom name"),
        ],
        default="FILENAME"
    )
    include_version_number: bpy.props.BoolProperty(name="Include Version Number", default=False)  # type: ignore
    custom_playblast_name:  bpy.props.StringProperty(name="Custom Name", default="playblast")  # type: ignore

    # ── Video ──────────────────────────────────────────────────────────────────
    file_format: bpy.props.EnumProperty(  # type: ignore
        name="File Format",
        items=[
            ('FFMPEG',   "FFmpeg Video", ""),
            ('AVI_JPEG', "AVI JPEG",     ""),
            ('AVI_RAW',  "AVI Raw",      ""),
        ],
        default='FFMPEG',
    )
    container: bpy.props.EnumProperty(  # type: ignore
        name="Container",
        items=[
            ('MPEG4',     "MPEG-4",    ""),
            ('AVI',       "AVI",       ""),
            ('QUICKTIME', "QuickTime", ""),
            ('MKV',       "Matroska",  ""),
        ],
        default='MPEG4',
    )
    video_codec: bpy.props.EnumProperty(  # type: ignore
        name="Video Codec",
        items=[
            ('H264',  "H.264",        ""),
            ('QTRLE', "QT Animation", ""),
        ],
        default='H264',
    )
    audio_codec: bpy.props.EnumProperty(  # type: ignore
        name="Audio Codec",
        items=[
            ('NONE', "No Audio", ""),
            ('AAC',  "AAC",      ""),
            ('MP3',  "MP3",      ""),
        ],
        default='NONE',
    )
    keyframe_interval: bpy.props.IntProperty(name="Keyframe Interval", default=18, min=1, max=500)  # type: ignore
    video_bitrate: bpy.props.IntProperty(name="Bitrate (Mbps)", default=50, min=1, max=500)  # type: ignore

    # ── Render ─────────────────────────────────────────────────────────────────
    use_viewport_shading: bpy.props.BoolProperty(  # type: ignore
        name="Use Viewport Shading", default=True,
        description="Render with viewport shading (OpenGL). Disable to use F12 render engine.",
    )
    viewport_shading: bpy.props.EnumProperty(  # type: ignore
        name="Viewport Shading",
        items=[
            ('WIREFRAME', "Wireframe", ""),
            ('SOLID',     "Solid",     ""),
            ('MATERIAL',  "Material",  ""),
            ('RENDERED',  "Rendered",  ""),
        ],
        default='SOLID'
    )
    resolution_percentage: bpy.props.IntProperty(  # type: ignore
        name="Resolution %", default=100, min=1, max=200, subtype='PERCENTAGE',
    )
    frame_rate: bpy.props.IntProperty(name="Frame Rate", default=24, min=1, max=240)  # type: ignore
    autoplay_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Autoplay After Render",
        default=True,
        description="Open the Blender video player and loop the playblast when done",
    )

    # ── Metadata (Burn-In) ─────────────────────────────────────────────────────
    burnin_enabled: bpy.props.BoolProperty(name="Enable Burn-In", default=True)  # type: ignore

    comment_dialog_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Add Comment on Playblast",
        description="Show comment dialog before each playblast render",
        default=True
    )

    comment_position: bpy.props.EnumProperty(  # type: ignore
        name="Comment Position",
        description="Where to inject {comment} in the overlay if not already placed manually",
        items=[
            ('TOP_LEFT',     "Top Left",      ""),
            ('TOP_CENTER',   "Top Center",    ""),
            ('TOP_RIGHT',    "Top Right",     ""),
            ('BOTTOM_LEFT',  "Bottom Left",   ""),
            ('BOTTOM_CENTER',"Bottom Center", ""),
            ('BOTTOM_RIGHT', "Bottom Right",  ""),
            ('NONE',         "Ne pas injecter", "Ne pas ajouter le commentaire automatiquement"),
        ],
        default='BOTTOM_CENTER'
    )

    meta_file:        bpy.props.BoolProperty(name="Filename",        default=True)  # type: ignore
    meta_frame_range: bpy.props.BoolProperty(name="Frame Range",     default=True)  # type: ignore
    meta_scene:       bpy.props.BoolProperty(name="Scene",           default=True)  # type: ignore
    meta_resolution:  bpy.props.BoolProperty(name="Resolution",      default=True)  # type: ignore
    meta_fps:         bpy.props.BoolProperty(name="FPS",             default=True)  # type: ignore
    meta_camera:      bpy.props.BoolProperty(name="Camera",          default=True)  # type: ignore
    meta_lens:        bpy.props.BoolProperty(name="Lens",            default=True)  # type: ignore
    meta_marker:      bpy.props.BoolProperty(name="Marker",          default=False)  # type: ignore
    meta_strip:       bpy.props.BoolProperty(name="Sequencer Strip", default=False)  # type: ignore
    meta_user:        bpy.props.BoolProperty(name="User",            default=True)  # type: ignore
    meta_hostname:    bpy.props.BoolProperty(name="Hostname",        default=False)  # type: ignore
    meta_date:        bpy.props.BoolProperty(name="Date",            default=True)  # type: ignore
    meta_memory:      bpy.props.BoolProperty(name="Memory Usage",    default=False)  # type: ignore
    meta_render_time: bpy.props.BoolProperty(name="Render Time",     default=False)  # type: ignore
    meta_threads:     bpy.props.BoolProperty(name="Thread Count",    default=False)  # type: ignore
    meta_comment:     bpy.props.BoolProperty(name="Comment / Note",  default=True)  # type: ignore
    meta_icon:        bpy.props.BoolProperty(name="Icon (Logo)",     default=True)  # type: ignore

    # ── Custom Layout ──────────────────────────────────────────────────────────
    overlay_top_left: bpy.props.StringProperty(  # type: ignore
        name="Top Left",
        description="Top-left corner text (supports placeholders like {file_name})",
        default="{file_name}"
    )

    overlay_top_center: bpy.props.StringProperty(  # type: ignore
        name="Top Center",
        description="Top-center text",
        default="{frame_range}"
    )

    overlay_top_right: bpy.props.StringProperty(  # type: ignore
        name="Top Right",
        description="Top-right corner text",
        default="{resolution} | {fps}fps"
    )

    overlay_bottom_left: bpy.props.StringProperty(  # type: ignore
        name="Bottom Left",
        description="Bottom-left corner text",
        default="{camera_name} | {camera_focal}mm"
    )

    overlay_bottom_center: bpy.props.StringProperty(  # type: ignore
        name="Bottom Center",
        description="Bottom-center text (reserved for comment by default)",
        default="{comment}"
    )

    overlay_bottom_right: bpy.props.StringProperty(  # type: ignore
        name="Bottom Right",
        description="Bottom-right corner text",
        default="{user} | {date} | {time}"
    )

    overlay_font_size: bpy.props.IntProperty(  # type: ignore
        name="Font Size",
        description="Overlay text font size",
        default=24,
        min=8,
        max=72
    )

    overlay_margin: bpy.props.IntProperty(  # type: ignore
        name="Margin",
        description="Horizontal padding from frame edge (pixels)",
        default=10,
        min=0,
        max=100
    )

    overlay_text_color: bpy.props.FloatVectorProperty(  # type: ignore
        name="Text Color",
        description="Overlay text color",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0
    )

    overlay_bg_color: bpy.props.FloatVectorProperty(  # type: ignore
        name="Background Color",
        description="Overlay background color",
        default=(0.0, 0.0, 0.0),
        subtype='COLOR',
        min=0.0,
        max=1.0
    )

    overlay_opacity: bpy.props.FloatProperty(  # type: ignore
        name="Opacity",
        description="Overlay background opacity (0.0 = transparent, 1.0 = opaque)",
        default=0.75,
        min=0.0,
        max=1.0,
        step=0.05,
        subtype='FACTOR'
    )

    # ── Tab selector ───────────────────────────────────────────────────────────
    prefs_tab: bpy.props.EnumProperty(  # type: ignore
        name="Tab",
        items=[
            ('OUTPUT',   "Output",         "Output folder and filename settings"),
            ('VIDEO',    "Video Settings", "Codec, format and bitrate"),
            ('RENDER',   "Render",         "Shading, resolution and frame rate"),
            ('METADATA', "Metadata",       "Burn-in overlay content"),
        ],
        default='OUTPUT',
    )

    # ── Draw ───────────────────────────────────────────────────────────────────
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        # Tab buttons — prop_enum draws one button per call with reliable text
        row = layout.row(align=True)
        row.scale_y = 1.3
        row.prop_enum(self, "prefs_tab", "OUTPUT")
        row.prop_enum(self, "prefs_tab", "VIDEO")
        row.prop_enum(self, "prefs_tab", "RENDER")
        row.prop_enum(self, "prefs_tab", "METADATA")
        layout.separator()

        if   self.prefs_tab == 'OUTPUT':   self._draw_output(layout)
        elif self.prefs_tab == 'VIDEO':    self._draw_video(layout)
        elif self.prefs_tab == 'RENDER':   self._draw_render(layout)
        elif self.prefs_tab == 'METADATA': self._draw_metadata(layout)

    def _draw_output(self, layout):
        box = layout.box()
        box.label(text="Output Folder", icon='FILE_FOLDER')
        box.prop(self, "output_folder_mode", text="Mode")
        if self.output_folder_mode == 'PROJECT':
            row = box.row()
            row.prop(self, "project_subfolder_enabled", text="Use Subfolder")
            if self.project_subfolder_enabled:
                row.prop(self, "project_subfolder_name", text="Name")
        elif self.output_folder_mode == 'SYSTEM':
            box.prop(self, "system_folder_path", text="Path")

        box2 = layout.box()
        box2.label(text="Playblast Name", icon='FILE_TEXT')
        box2.prop(self, "playblast_name_mode", text="Mode")
        if self.playblast_name_mode == 'CUSTOM':
            box2.prop(self, "custom_playblast_name", text="Name")
        else:
            box2.prop(self, "include_version_number")

    def _draw_video(self, layout):
        box = layout.box()
        box.label(text="Video Settings", icon='FILE_MOVIE')
        
        # Video settings locked to FFmpeg MP4
        col = box.column(align=True)
        col.enabled = False
        col.prop(self, "file_format")
        col.prop(self, "container")
        col.prop(self, "video_codec")
        col.prop(self, "audio_codec")
        col.prop(self, "keyframe_interval")
        col.prop(self, "video_bitrate")
        
        # Info message
        box.label(text="Currently locked to FFmpeg MP4 H.264", icon='INFO')

    def _draw_render(self, layout):
        box = layout.box()
        box.label(text="Viewport", icon='RENDER_STILL')
        box.prop(self, "use_viewport_shading")
        if self.use_viewport_shading:
            box.prop(self, "viewport_shading", text="Shading")
        else:
            box.label(text="Uses F12 render engine", icon='INFO')

        box2 = layout.box()
        box2.label(text="Resolution & Frame Rate", icon='FULLSCREEN_ENTER')
        box2.prop(self, "resolution_percentage", text="Resolution %", slider=True)
        box2.prop(self, "frame_rate",            text="Frame Rate")

        box3 = layout.box()
        box3.label(text="Playback", icon='PLAY')
        box3.prop(self, "autoplay_enabled", text="Autoplay After Render")

    def _draw_metadata(self, layout):
        box = layout.box()
        box.label(text="Burn-In Overlay", icon='FONT_DATA')
        box.prop(self, "burnin_enabled", text="Enable Burn-In")

        if not self.burnin_enabled:
            return

        box1 = layout.box()
        box1.label(text="Comment", icon='GREASEPENCIL')
        box1.prop(self, "comment_dialog_enabled", text="Add Comment on Playblast")

        # ─── Custom Layout ────────────────────────────────────────────────────
        # TEMPORARILY DISABLED - Coming in a future version
        box2 = layout.box()
        box2.label(text="Custom Layout (Coming Soon)", icon='OVERLAY')
        col = box2.column(align=True)
        col.enabled = False
        col.label(text="Position Configuration:", icon='LINENUMBERS_ON')
        col.prop(self, "overlay_top_left",      text="Top Left")
        col.prop(self, "overlay_top_center",    text="Top Center")
        col.prop(self, "overlay_top_right",     text="Top Right")
        col.separator(factor=0.5)
        col.prop(self, "overlay_bottom_left",   text="Bottom Left")
        col.prop(self, "overlay_bottom_center", text="Bottom Center")
        col.prop(self, "overlay_bottom_right",  text="Bottom Right")

        col.separator(factor=0.5)
        col.label(text="Appearance:", icon='OVERLAY')
        col.prop(self, "overlay_font_size", text="Font Size")
        col.prop(self, "overlay_margin",    text="Margin")
        col.prop(self, "overlay_text_color", text="Text Color")
        col.prop(self, "overlay_bg_color",   text="Background Color")
        col.prop(self, "overlay_opacity",    text="Opacity")

        # ─── Available Placeholders ───────────────────────────────────────────
        box3 = layout.box()
        box3.label(text="Available Placeholders", icon='INFO')
        
        col_info = box3.column(align=False)
        col_info.scale_y = 0.9
        
        placeholders = [
            ("File name",       "{file_name}"),
            ("Frame range",     "{frame_range}"),
            ("Resolution",      "{resolution}"),
            ("FPS",             "{fps}"),
            ("Camera",          "{camera_name}"),
            ("Lens",            "{camera_focal}"),
            ("User",            "{user}"),
            ("Date",            "{date}"),
            ("Time",            "{time}"),
            ("Comment",         "{comment}"),
            ("Scene",           "{scene_name}"),
            ("Marker",          "{marker}"),
            ("Sequencer Strip", "{sequencer_strip}"),
            ("Hostname",        "{hostname}"),
            ("Memory Usage",    "{memory_usage}"),
            ("Render Time",     "{render_time}"),
            ("Thread Count",    "{thread_count}"),
        ]

        for label, placeholder in placeholders:
            row = col_info.row(align=True)
            row.label(text=f"{label}  {placeholder}")
            op = row.operator("bp.overlay_copy_placeholder", text="", icon='COPYDOWN')
            op.placeholder = placeholder
        
        # ─── Usage Guide ──────────────────────────────────────────────────────
        box4 = layout.box()
        box4.label(text="How to Use Placeholders", icon='HELP')
        col_help = box4.column(align=False)
        col_help.scale_y = 0.85
        col_help.label(text="Copy placeholders to your position fields.")
        col_help.label(text="Example: Top Left = \"{file_name}\" or \"{file_name} - {date}\"")
        col_help.label(text="Avoid using | separator; use space or custom text instead")
        col_help.label(text="Example: \"{file_name} v{file_version}\" (instead of \"{file_name}|v{file_version}\")")
