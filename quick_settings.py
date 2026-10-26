"""BetterPlayblast Quick Settings - Scene-level overrides for temporary playblast changes"""

import bpy


class BP_QuickSettings(bpy.types.PropertyGroup):
    """Per-scene Quick Settings that override addon preferences when enabled"""

    # ═══════════════════════════════════════════════════════════════════════════
    # VERSION TRACKING & COMPATIBILITY
    # ═══════════════════════════════════════════════════════════════════════════
    current_version: bpy.props.IntProperty(  # type: ignore
        name="Version",
        description="Current playblast version number",
        default=1,
        min=1
    )

    last_playblast_name: bpy.props.StringProperty(  # type: ignore
        name="Last Playblast",
        description="Name of the last rendered playblast",
        default=""
    )

    version_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Enable Version",
        default=True
    )

    version_number: bpy.props.IntProperty(  # type: ignore
        name="Version Number",
        default=1,
        min=1,
        max=9999
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # VIDEO SETTINGS
    # ═══════════════════════════════════════════════════════════════════════════
    file_format: bpy.props.EnumProperty(  # type: ignore
        name="File Format",
        items=[
            ('FFMPEG', "FFmpeg Video", "FFmpeg video encoder"),
            ('AVI_JPEG', "AVI JPEG", "AVI with JPEG compression"),
            ('AVI_RAW', "AVI Raw", "Uncompressed AVI"),
        ],
        default='FFMPEG'
    )

    container: bpy.props.EnumProperty(  # type: ignore
        name="Container",
        items=[
            ('MPEG4', "MPEG-4", "MPEG-4 container (.mp4)"),
            ('AVI', "AVI", "AVI container (.avi)"),
            ('QUICKTIME', "QuickTime", "QuickTime container (.mov)"),
        ],
        default='MPEG4'
    )

    video_codec_fmt: bpy.props.EnumProperty(  # type: ignore
        name="Video Codec",
        items=[
            ('H264', "H.264", "H.264/AVC — universal, high quality"),
            ('QT_ANIMATION', "QT Animation", "QuickTime Animation — lossless"),
        ],
        default='H264'
    )

    audio_codec: bpy.props.EnumProperty(  # type: ignore
        name="Audio Codec",
        items=[
            ('NO_AUDIO', "No Audio", "No audio track"),
            ('AAC', "AAC", "Advanced Audio Coding"),
            ('MP3', "MP3", "MPEG Layer 3 audio"),
        ],
        default='NO_AUDIO'
    )

    keyframe_interval: bpy.props.IntProperty(  # type: ignore
        name="Keyframe Interval",
        description="Distance between keyframes (GOP size)",
        default=18,
        min=1,
        max=500
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # AUDIO SETTINGS
    # ═══════════════════════════════════════════════════════════════════════════
    include_audio_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Include Audio",
        description="Override addon audio codec for this playblast",
        default=False
    )

    include_audio_codec: bpy.props.EnumProperty(  # type: ignore
        name="Audio Codec",
        items=[
            ('NO_AUDIO', "No Audio", "No audio track"),
            ('AAC', "AAC", "Advanced Audio Coding"),
            ('MP3', "MP3", "MPEG Layer 3 audio"),
        ],
        default='AAC'
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # RESOLUTION
    # ═══════════════════════════════════════════════════════════════════════════
    resolution_override_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Resolution",
        description="Override addon resolution percentage",
        default=False
    )

    resolution_percentage: bpy.props.IntProperty(  # type: ignore
        name="Resolution %",
        default=100,
        min=1,
        max=200,
        subtype='PERCENTAGE'
    )

    # Legacy compatibility
    resolution_override: bpy.props.BoolProperty(  # type: ignore
        name="Override Resolution",
        default=False
    )

    resolution_pct: bpy.props.IntProperty(  # type: ignore
        name="Resolution %",
        default=100,
        min=1,
        max=200,
        subtype='PERCENTAGE'
    )

    resize_method: bpy.props.EnumProperty(  # type: ignore
        name="Resize Method",
        items=[
            ('PERCENTAGE', "Resolution Percentage", "Render at a percentage of the project resolution"),
            ('KEEP', "Keep Project Resolution", "Use the project's full resolution"),
        ],
        default='KEEP'
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # VIEWPORT SHADING
    # ═══════════════════════════════════════════════════════════════════════════
    shading_override_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Viewport Shading",
        description="Override viewport shading for playblast",
        default=False
    )

    viewport_shading: bpy.props.EnumProperty(  # type: ignore
        name="Shading",
        items=[
            ('WIREFRAME', "Wireframe", ""),
            ('SOLID', "Solid", ""),
            ('MATERIAL', "Material", ""),
            ('RENDERED', "Rendered", ""),
        ],
        default='SOLID'
    )

    # Legacy compatibility
    shading_override: bpy.props.BoolProperty(  # type: ignore
        name="Override Shading",
        default=False
    )

    shading_type: bpy.props.EnumProperty(  # type: ignore
        name="Shading Type",
        items=[
            ('WIREFRAME', "Wireframe", "", 'SHADING_WIRE', 0),
            ('SOLID', "Solid", "", 'SHADING_SOLID', 1),
            ('MATERIAL', "Material", "", 'SHADING_TEXTURE', 2),
            ('RENDERED', "Rendered", "", 'SHADING_RENDERED', 3),
        ],
        default='SOLID'
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # FRAME RANGE
    # ═══════════════════════════════════════════════════════════════════════════
    frame_range_override_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Frame Range",
        description="Override playblast frame range",
        default=False
    )

    frame_start: bpy.props.IntProperty(  # type: ignore
        name="Start Frame",
        default=1
    )

    frame_end: bpy.props.IntProperty(  # type: ignore
        name="End Frame",
        default=250
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # RENDER OPTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    overlays_override: bpy.props.BoolProperty(  # type: ignore
        name="Override Overlays",
        default=False
    )

    overlays_mode: bpy.props.EnumProperty(  # type: ignore
        name="Overlays",
        items=[
            ('ALL', "Hide All Overlays", "Hide all viewport overlays"),
            ('BONES', "Hide Only Bones", "Hide bone overlays only"),
            ('ALL_EXCEPT_BG', "Hide All Except Camera Background Images", "Keep camera background images visible"),
            ('NONE', "Don't Overwrite Scene Settings", "Keep current overlay settings as-is"),
        ],
        default='NONE'
    )

    autoplay_when_done: bpy.props.BoolProperty(  # type: ignore
        name="Autoplay When Done",
        description="Automatically play the playblast when rendering is complete",
        default=False
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # BURN-IN
    # ═══════════════════════════════════════════════════════════════════════════
    burnin_override_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Burn-In",
        description="Override burn-in settings for this playblast",
        default=False
    )

    burnin_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Enable Burn-In",
        default=True
    )

    burnin_font_path: bpy.props.StringProperty(  # type: ignore
        name="Font",
        description="Path to a custom font file for burn-in text",
        default="",
        subtype='FILE_PATH'
    )

    burnin_text_position: bpy.props.EnumProperty(  # type: ignore
        name="Text Position",
        items=[
            ('TOP_LEFT', "Top Left", ""),
            ('TOP_CENTER', "Top Center", ""),
            ('TOP_RIGHT', "Top Right", ""),
            ('BOTTOM_LEFT', "Bottom Left", ""),
            ('BOTTOM_CENTER', "Bottom Center", ""),
            ('BOTTOM_RIGHT', "Bottom Right", ""),
        ],
        default='BOTTOM_LEFT'
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # UI STATE — SECTION EXPAND TOGGLES
    # ═══════════════════════════════════════════════════════════════════════════
    qs_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Quick Settings Expanded",
        default=True
    )

    vs_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Video Settings",
        default=True
    )

    au_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Audio Settings",
        default=False
    )

    res_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Resolution",
        default=True
    )

    ro_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Render Options",
        default=True
    )

    bi_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Burn-In",
        default=True
    )

    st_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Settings",
        default=False
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # OVERLAY CUSTOMIZATION — Viewport Preview & Custom Positioning
    # ═══════════════════════════════════════════════════════════════════════════
    overlay_preview_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Preview Overlay in Viewport",
        description="Show overlay preview in 3D viewport camera view (may impact performance)",
        default=False
    )

    overlay_custom_enabled: bpy.props.BoolProperty(  # type: ignore
        name="Custom Overlay Layout",
        description="Enable custom overlay positioning instead of default layout",
        default=True
    )

    overlay_template: bpy.props.EnumProperty(  # type: ignore
        name="Overlay Template",
        description="Quick template preset for overlay layout",
        items=[
            ('minimal', "Minimal", "Filename + Version + Date + Resolution"),
            ('standard', "Standard", "Default balanced layout"),
            ('production', "Production", "Complete production specs"),
            ('tech_specs', "Technical Specs", "Detailed technical information"),
            ('minimal_bottom', "Bottom Only", "All info in bottom bar"),
            ('custom', "Custom", "Use custom text below"),
        ],
        default='standard'
    )

    # Custom overlay positions — each can contain text with placeholders
    overlay_top_left: bpy.props.StringProperty(  # type: ignore
        name="Top Left",
        description="Text for top-left corner (supports placeholders like {file_name}, {datetime})",
        default="{file_name}"
    )

    overlay_top_center: bpy.props.StringProperty(  # type: ignore
        name="Top Center",
        description="Text for top-center",
        default="{frame_range}"
    )

    overlay_top_right: bpy.props.StringProperty(  # type: ignore
        name="Top Right",
        description="Text for top-right corner",
        default="{resolution} | {fps}fps"
    )

    overlay_bottom_left: bpy.props.StringProperty(  # type: ignore
        name="Bottom Left",
        description="Text for bottom-left corner",
        default="{camera_name} | {camera_focal}mm"
    )

    overlay_bottom_center: bpy.props.StringProperty(  # type: ignore
        name="Bottom Center",
        description="Text for bottom-center",
        default=""
    )

    overlay_bottom_right: bpy.props.StringProperty(  # type: ignore
        name="Bottom Right",
        description="Text for bottom-right corner",
        default="{user} | {date} | {time}"
    )

    # Overlay appearance options
    overlay_opacity: bpy.props.FloatProperty(  # type: ignore
        name="Opacity",
        description="Overlay background opacity (0.0 = transparent, 1.0 = opaque)",
        default=0.75,
        min=0.0,
        max=1.0,
        step=0.05,
        subtype='FACTOR'
    )

    overlay_text_color: bpy.props.FloatVectorProperty(  # type: ignore
        name="Text Color",
        description="Overlay text color",
        default=(1.0, 1.0, 1.0),  # White
        subtype='COLOR',
        min=0.0,
        max=1.0
    )

    overlay_bg_color: bpy.props.FloatVectorProperty(  # type: ignore
        name="Background Color",
        description="Overlay background color",
        default=(0.0, 0.0, 0.0),  # Black
        subtype='COLOR',
        min=0.0,
        max=1.0
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

    # ═══════════════════════════════════════════════════════════════════════════
    # COMMENT — popup before playblast, injected into overlay via {comment}
    # ═══════════════════════════════════════════════════════════════════════════
    overlay_show_icons: bpy.props.BoolProperty(  # type: ignore
        name="Show Icons",
        description="Show icons next to metadata labels in the overlay (default layout only)",
        default=True
    )

    ph_expanded: bpy.props.BoolProperty(  # type: ignore
        name="Placeholder Reference",
        description="Show available placeholder codes",
        default=False
    )
