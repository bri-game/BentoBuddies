# Bento Buddies — delivery contract

Fantasy: pack a thoughtful picnic for three animal friends. Emotional thesis: “Everything fits, and I remembered what my friend likes.” Pressure comes from spatial reasoning and ingredient relationships, never a timer.

Android portrait; Cocos Creator 3.8.8; TypeScript truth model; Vietnamese UI. Drag ingredients, tap to select, rotate using a stable button, tap a cell to place as accessible alternate input. Reversible placement, undo, reset, explicit lid/serve commit. QA package com.bentobuddies.game.qa, production reservation com.bentobuddies.game. Version 0.1.0 / 1, debug-signed QA arm64. Offline, no ads, IAP, energy or accounts.

Scope: 24 validated authored packing puzzles, 8 ingredient identities, 3 friends, rules introduced separately (rice touches vegetables; ice never touches hot food; strawberry touches box edge), picnic album of completed arrangements, saved unlocks, replay, contextual tutorial, hints, persistent music/SFX switches, Android back/pause. No optimality or unique-solution claims. Daily live content, compression, dividers and monetization are future scope.

Gates: deterministic tests and solution replay/structural variety audit; phone-scale presentation including short/tall viewports; Cocos export and Gradle debug assembly; inspect exact APK; authorized physical-device cold start, inputs, wrong serving/retry, success/unlock/save, settings/background/back and rich content; retain screenshots and logcat. Delivery report records hash/signing/device/gaps.

# Art bible
Warm paper cream #FFF5E4, cocoa ink #51382E, coral #E88068 for primary actions, leaf green #718B5B for success, biscuit #E9CDA9 for wooden tray. Rounded cut-paper shapes, gentle offset shadows, matte surfaces, sparse grain only on illustration. Food silhouettes and small ingredient letters distinguish types independently of color. Unselected food has dark contour, selected uses cream/coral halo, invalid placement crossed outline, successful meal has sparkles and smiling friend. Quiet tray background. Typography: bold friendly system sans, 36–54 title, 22–28 main, >=18 secondary at 720 design width. Food rendered as scalable vector art; original generated picnic cover carries same palette. Touch targets >=64 design units. Content vertically centered inside fitted 720x1280 safe canvas with generous top/bottom margin.
