# Picnic toybox reskin — v0.2.0

User direction: all buttons, icons and backgrounds should look like a game; replace flat app-like surfaces with ImageGen art. Keep existing packing rules, touch geometry, level data and saved progress.

Visual direction: tactile, hand-painted 2.5D picnic toybox. Honey-colored wooden frames, coral jelly/enamel primary buttons, cream stitched fabric secondary buttons, illustrated food and animal portraits, brass/wood action icons, grassy meadow and gingham cloth scenery. Warm highlights from upper left, short soft shadows, chunky silhouettes and cocoa contours. Clear quiet regions behind board and labels. Button labels remain runtime Vietnamese text for sharpness and localization. Primary/secondary/selected/disabled/pressed states share the generated skin; pressed uses scale; used ingredients show a check badge and muted previews. Keep all original UI hit rectangles, enlarge decorative visual backgrounds only.

Assets: original ImageGen portrait background, transparent UI atlas, transparent action-icon atlas, transparent food/mascot atlas, transparent title logo and Android icon. Source atlases preserved unchanged inside assets/resources/art/v2; runtime SpriteFrames extract alpha-trimmed rectangles recorded in atlas.json. PNG and runtime tint/scaling are presentation only.
