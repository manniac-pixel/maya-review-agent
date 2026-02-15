# Maya Stitch Prompts — v2 (Dark Mode + Updated Branding)

All 12 screen prompts for Google Stitch. Login screens use white backgrounds (matching `screen.png`). All inner app screens use Dark Navy (#112432) backgrounds.

**Workflow:** Sketch-to-UI (wireframe + prompt) for 4 hero screens. Text-to-UI for 8 supporting screens.

---

## Brand Context (Prefix Every Prompt)

> **Brand Context:**
> - **Primary:** Maya Green (#75EEA5) — buttons, toggles, links, key accents.
> - **Dark Background:** Dark Navy (#112432) — main background for app screens.
> - **Card Surface:** Slightly lighter dark (#1A3042) with subtle border (#243B4D).
> - **Purple Accent:** (#6F42C1) — used sparingly for premium badges or special features only.
> - **Success:** Jade (#00B463). **Warning:** Burning Sand (#D69474). **Error:** Red (#FF3B30).
> - **Headline Font:** Tuka (bold, quirky, bird-beak ink traps). Fallback: Unbounded or Syne.
> - **Body Font:** Cerebri Sans Pro (clean, geometric). Fallback: Plus Jakarta Sans.
> - **Text on dark:** White (#FFFFFF) for primary, gray (#9CA3AF) for secondary.
> - **Buttons:** Full-width pill shape (border-radius: 50px). Maya Green (#75EEA5) solid fill, dark text (#112432).
> - **Rounded corners:** 16px for cards, 12px for inputs, 50px for buttons/pills.
> - **Vibe:** "Sleek but cheerful" — Gen Z fintech, high contrast, 3D where appropriate.
> - **No bottom tab bars** on any detail/inner screen.

---

## Flow A: Frictionless Login (3 Screens) — WHITE BACKGROUND

### Screen 1: Login_Splash ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `screen.png`

**Stitch Prompt:**
> A real iOS app screen. Login screen for a fintech app called Maya. White background (#FFFFFF). Do NOT add a bottom tab bar.
>
> Top section (centered, 80px below status bar):
> Maya app icon — a black rounded square (120px, border-radius: 28px) with the word "maya" in lowercase Maya Green (#75EEA5) text inside. Centered horizontally.
>
> Below icon (16px gap): "Welcome back" in Tuka font or a bold quirky sans-serif (28pt, black #000000), centered. Below that (8px gap): "Sign in to your account" in Cerebri Sans Pro regular (16pt, #9CA3AF), centered.
>
> Middle section (40px below subtitle):
> A centered pill-shaped outlined button "Unlock with FaceID" — thin border (#E5E7EB), no fill, border-radius 50px, padding 14px 32px. FaceID smiley icon on the left, black text (16pt).
>
> Below (24px gap): A divider — thin horizontal line (#E5E7EB) with "OR" text centered in gray (#9CA3AF), uppercase, 12pt.
>
> Below divider (24px gap): "MOBILE NUMBER" label (12pt, uppercase, #9CA3AF, left-aligned, 24px left margin). Below (8px): Full-width input field — rounded rectangle (border-radius: 12px), thin border (#E5E7EB), background #F9FAFB, placeholder "09XX XXX XXXX" in #9CA3AF, height 52px, 24px horizontal margin.
>
> Below input (8px): Row with "Register" in Maya Green (#75EEA5) bold 14pt left-aligned, "Forgot Number?" in #9CA3AF regular 14pt right-aligned. Both at 24px horizontal margin.
>
> Bottom (24px from bottom edge, 24px horizontal margin): Full-width pill button "Login" — Maya Green (#75EEA5) solid fill, text "#112432" bold 16pt, border-radius 50px, height 56px. Subtle shadow (0 4px 12px rgba(117, 238, 165, 0.3)).
>
> No other elements. Clean, lots of whitespace. Centered layout. Matches a production banking app.

---

### Screen 2: Login_Biometric
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Biometric verification screen. White background (#FFFFFF). No navigation bar. No bottom tab bar.
>
> Vertically centered on screen:
> A FaceID icon (64px) in dark (#112432), centered horizontally. Below (24px gap): a thin circular ring (80px diameter, 2px stroke, Maya Green #75EEA5) — this is a loading/progress indicator. Below ring (16px gap): "Verifying your identity..." in Cerebri Sans Pro regular 16pt, #9CA3AF, centered.
>
> Bottom section (80px from bottom): Text "Use password instead" in #9CA3AF regular 14pt, underlined, centered.
>
> Nothing else. Pure white. Single focal point. Calm, minimal.

---

### Screen 3: Login_Fallback
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Manual login form. White background (#FFFFFF). No bottom tab bar.
>
> Top: iOS navigation bar with back chevron (<) in #112432, left-aligned. No title text in the nav bar. Thin 1px bottom line (#F3F4F6).
>
> Header (24px left margin, 24px below nav): "Login" in Tuka or bold quirky sans-serif (28pt, #000000), left-aligned. Below (8px): "Enter your credentials" in Cerebri Sans Pro regular (16pt, #9CA3AF).
>
> Form section (24px horizontal margin, 24px below header):
> Field 1: "MOBILE NUMBER" label (12pt, uppercase, #9CA3AF). Below (8px): Input field — 12px border-radius, 1px border #E5E7EB, background #F9FAFB, placeholder "+63 9XX XXX XXXX", height 52px.
>
> Field 2 (16px below): "PASSWORD" label (12pt, uppercase, #9CA3AF). Below (8px): Input field — same style, placeholder "••••••••", eye icon on the right in #9CA3AF for show/hide toggle.
>
> Below password field (8px): "Forgot Password?" in Maya Green (#75EEA5) bold 14pt, right-aligned.
>
> Below (32px): Divider — "OR" centered with gray lines.
>
> Below (16px): Full-width pill outlined button "Request OTP" — no fill, 1px border #E5E7EB, #112432 text, 50px radius, height 48px.
>
> Bottom (24px from bottom, 24px horizontal margin): Full-width pill button "Login" — Maya Green (#75EEA5) solid, #112432 text bold, 50px radius, height 56px.

---

## Flow B: Transparent Transactions (3 Screens) — DARK BACKGROUND

### Screen 4: Transaction_Pending ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `transaction_pending_wireframe_hifi_ios.png`

**Stitch Prompt:**
> A real iOS app screen. Transaction pending screen. Dark background (#112432). All text is white or light gray. Do NOT add a bottom tab bar. Do NOT add navigation with Home, Activity, Scan, Cards, or Profile.
>
> Top: Navigation bar on dark background. Left: back arrow (<) in white. Center: "Transaction Pending" in Tuka or bold quirky font (17pt, white #FFFFFF). Thin 1px bottom line (#243B4D).
>
> Section 1 — Amount (centered, 24px below nav):
> "₱2,500.00" in bold 32pt white (#FFFFFF), centered. Below (8px): "Cash In via GCash" in 14pt #9CA3AF, centered. Below (16px): pill badge "Pending" — background #D69474, white text 12pt bold, border-radius 50px, padding 4px 12px.
>
> Section 2 — Timer (centered, 24px below badge):
> A rounded container (180px wide, 64px tall, border-radius 12px, background #1A3042, border 1px #243B4D). Inside: "2:01" in monospaced font, 36pt bold, color #D69474. Nothing else in the container — no icons.
>
> Section 3 — Progress stepper (24px below timer, 24px left padding):
> Row 1: 24px solid green circle (#00B463) with white checkmark. 12px right: "Request Sent" in 16pt bold white. Below: vertical 2px line in #00B463, 28px tall.
> Row 2: Same green circle + checkmark. "Processing" in 16pt bold white. Below: vertical 2px line — top half #00B463, bottom half #243B4D, 28px tall.
> Row 3: 24px circle, no fill, 2px border #D69474. "Awaiting Confirmation" in 16pt regular #9CA3AF.
>
> Section 4 — Notify toggle (24px below stepper):
> Full-width row with 1px top border #243B4D, 24px horizontal padding, 16px vertical padding. Left: "Notify me when completed" in 16pt white. Right: iOS toggle switch, ON state — Maya Green (#75EEA5) track, white knob.
>
> Nothing else below. No tab bar. Screen ends with dark space. This is a detail screen.

---

### Screen 5: Transaction_Details
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Transaction details screen. Dark background (#112432). No bottom tab bar.
>
> Top: Nav bar on dark. Back chevron in white. "Transaction Details" centered in bold 17pt white. Thin 1px line (#243B4D).
>
> Amount section (centered, 24px below nav):
> "₱2,500.00" in bold 36pt white, centered. Below (8px): "Cash In via GCash" in 14pt #9CA3AF. Below (12px): pill badge "Processing" — #D69474 background, white text 12pt bold, 50px radius.
>
> Details card (24px horizontal margin, 24px below badge):
> Dark card background (#1A3042), border 1px #243B4D, border-radius 16px, padding 20px.
> - Row: "From" (14pt, #9CA3AF, left) — "GCash Wallet" (16pt, white, right). Full width, space-between.
> - Divider: 1px line #243B4D.
> - Row: "To" — "Maya Savings"
> - Divider.
> - Row: "Reference" — "#MYA-2024-78291" (14pt, #9CA3AF value)
> - Divider.
> - Row: "Date" — "Feb 15, 2026, 2:41 PM"
>
> Progress bar (inside card, 16px below last row):
> Horizontal bar, full width, 4px height, 50px radius. Left 2/3 filled #00B463, right 1/3 #243B4D.
>
> Bottom (24px from bottom, 24px margin): Full-width pill outlined button "Report an Issue" — no fill, 1px border #243B4D, white text, 50px radius, height 48px.

---

### Screen 6: Transaction_Complete
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Transaction success screen. Dark background (#112432). No bottom tab bar.
>
> Hero section (centered, top third of screen):
> A solid green circle (80px, #00B463) with a white checkmark icon inside, centered. Below (16px): "Transfer Complete!" in Tuka or bold quirky font (28pt, white), centered. Below (8px): "₱2,500.00 received by Maya Savings" in 16pt #9CA3AF, centered.
>
> Receipt card (24px margin, 24px below subtitle):
> Dark card (#1A3042), border 1px #243B4D, border-radius 16px, padding 20px.
> - Row: "Reference" (14pt, #9CA3AF) — "#MYA-2024-78291" (16pt, white)
> - Divider (1px #243B4D).
> - Row: "Date" — "Feb 15, 2026, 2:43 PM"
> - Divider.
> - Row: "Fee" — "Free" (in #00B463)
>
> Toggle row (24px margin, 16px below card):
> Dark card (#1A3042), border 1px #243B4D, 16px radius, 16px padding. "Send receipt via email" in 16pt white, left. iOS toggle, Maya Green (#75EEA5) ON state, right.
>
> Bottom CTAs (24px margin, stacked, 12px gap, 24px from bottom):
> Primary pill: "Done" — Maya Green (#75EEA5) solid, #112432 text bold, 50px radius, 56px height.
> Text link: "View in Transaction History" — #00B463, 14pt, centered.

---

## Flow C: Accessible Support (3 Screens) — DARK BACKGROUND

### Screen 7: Help_Center_Home ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `help_center_wireframe_hifi_ios.png`

**Stitch Prompt:**
> A real iOS app screen. Help Center home screen. Dark background (#112432). No bottom tab bar.
>
> Top: Nav bar on dark. "Help Center" centered in bold 17pt white. Thin 1px line (#243B4D).
>
> My Tickets section (24px margin, 24px below nav):
> Label "MY TICKETS" (12pt, uppercase, #9CA3AF, bold, letter-spacing 0.5px).
> Below (12px): Ticket card — dark surface (#1A3042), border 1px #243B4D, border-radius 16px, padding 20px.
> Inside card:
> - "Ticket #1234" in bold 18pt white.
> - Status pill "Investigating" — #D69474 background, white text 12pt bold, 50px radius, padding 4px 12px.
> - "Submitted 2 hours ago" in 12pt #9CA3AF.
> - Right chevron (›) in #9CA3AF.
>
> Top Questions section (24px below ticket card):
> "Top Questions" in bold 20pt white.
> Below (12px): Dark grouped list (#1A3042, border 1px #243B4D, border-radius 16px):
> - "How to reset password?" (16pt, white) + chevron › (#9CA3AF). Padding 16px 20px.
> - Divider (1px #243B4D, inset 20px left).
> - "View recent transactions" + chevron.
> - Divider.
> - "Report lost card" + chevron.
> - Divider.
> - "Change contact information" + chevron.
> - Divider.
> - "Payment options" + chevron.
>
> Bottom (24px from bottom, 24px margin): Full-width pill button "Chat with Support" — Dark Navy text on Maya Green (#75EEA5) fill, bold, headset icon left of text, 50px radius, 56px height.

---

### Screen 8: Help_Ticket_Details
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Support ticket detail screen. Dark background (#112432). No bottom tab bar.
>
> Top: Nav bar on dark. Back chevron white. "Ticket #1234" centered bold 17pt white. Line (#243B4D).
>
> Status card (24px margin, 16px below nav):
> Dark card (#1A3042), border 1px #243B4D, 16px radius, 20px padding.
> - "Unable to complete cash-in" (18pt, bold, white).
> - Status pill "Investigating" — #D69474 pill, white text 12pt.
> - "Priority: High" — small red dot (#FF3B30, 6px) + text 14pt #9CA3AF.
>
> Activity section (24px margin, 24px below card):
> "Activity" in bold 16pt white. Below (16px):
> Timeline with 2px left border line (#243B4D), each entry indented 24px from left:
>
> Entry 1: Small circle (8px, filled #00B463) on the line. Right: "Ticket Created" bold 14pt white. Below: "Feb 15, 2:30 PM" 12pt #9CA3AF. Below: "You reported: Cash-in from GCash stuck at processing for 30 minutes." 14pt #9CA3AF.
>
> Entry 2 (24px below): Circle (8px, #00B463). "Under Review" bold 14pt white. "Feb 15, 2:45 PM". "Agent Maria assigned to your case."
>
> Entry 3 (24px below): Circle (8px, #D69474 — current). "Investigating" bold 14pt white. "Feb 15, 3:00 PM". "We're checking with our payment partner."
>
> Bottom CTAs (24px margin, stacked, 12px gap, 24px from bottom):
> Primary pill: "Add a Comment" — Maya Green (#75EEA5) solid, #112432 text, 50px radius, 56px height.
> Secondary pill: "Call Support" — no fill, 1px border #243B4D, white text, phone icon, 50px radius, 48px height.

---

### Screen 9: Help_Chat_Support
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Live chat screen. Dark background (#112432 for chrome, #0D1B27 for chat area). No bottom tab bar.
>
> Top: Nav bar on dark (#112432). Back chevron white. Left of center: "Chat with Maya" bold 17pt white + green dot (6px, #00B463). Below title: "Support Agent" 12pt #9CA3AF.
>
> Chat area (background #0D1B27, scrollable):
>
> Agent bubble (left-aligned): Dark card (#1A3042), border-radius 18px (bottom-left: 4px), padding 12px 16px. Text: "Hi! I'm here to help. I can see your ticket about the pending cash-in. Let me check the status." 14pt white. Below bubble: "3:05 PM" 10pt #9CA3AF.
>
> User bubble (right-aligned, 16px below): Maya Green (#75EEA5) background, border-radius 18px (bottom-right: 4px), padding 12px 16px. Text: "Thanks! It's been stuck for an hour now." 14pt #112432. Below: "3:06 PM" 10pt #9CA3AF.
>
> Agent bubble: "I've escalated this to our payments team. You should see the funds in 15-30 minutes."
>
> Typing indicator (left-aligned): Dark card (#1A3042), 3 gray dots (#9CA3AF) with subtle animation.
>
> Quick replies (horizontal scroll, 16px above input): Pill chips — "Send screenshot", "Check balance", "Escalate to manager" — no fill, 1px border #243B4D, white text 12pt, 50px radius, padding 8px 16px.
>
> Input bar (bottom, background #112432, 1px top border #243B4D):
> Rounded input field (#1A3042 background, 50px radius, 44px height), placeholder "Type a message..." in #9CA3AF, 14pt. Right side: send arrow icon in Maya Green (#75EEA5). Left side: attachment icon in #9CA3AF.

---

## Flow D: Security Center (3 Screens) — DARK BACKGROUND

### Screen 10: Security_Dashboard ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `security_center_wireframe_hifi_ios.png`

**Stitch Prompt:**
> A real iOS app screen. Security Center dashboard. Dark background (#112432). No bottom tab bar.
>
> Top: "Security Center" in Tuka or bold quirky font (28pt, white), left-aligned, 24px margin, 16px below status bar. No back button — this is a main section.
>
> Hero section (centered, 32px below title):
> A large shield shape (180px tall) — outlined in Maya Green (#75EEA5) with 3px stroke, filled with a subtle gradient from #1A3042 to #112432. The shield has a slight 3D look with a thin highlight edge on the upper-left.
> Inside the shield, centered: "80%" in Tuka or bold quirky font (48pt, white). Below the number: "Secure" in Cerebri Sans Pro regular (16pt, #9CA3AF).
> Below shield (12px): "Good. 2 actions recommended." in 14pt #9CA3AF, centered.
>
> Kill Switch card (24px margin, 32px below shield text):
> Dark card (#1A3042), border 1px #243B4D, border-radius 16px, padding 20px. Flex row, space-between.
> Left: "Kill Switch" bold 18pt white. Below: "Instantly lock your account." 14pt #9CA3AF.
> Right: iOS toggle switch — Red (#FF3B30) track in ON state, white knob. Standard iOS size (51x31px).
>
> Active Sessions card (24px margin, 12px below Kill Switch card):
> Same dark card style. Flex row.
> Left: Lock icon (white, 20px). "Active Sessions" bold 16pt white.
> Right: "(3)" in #9CA3AF + chevron › in #9CA3AF.
>
> Nothing else below. Dark background continues.

---

### Screen 11: Security_KillSwitch_Confirm
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Kill Switch confirmation modal over the Security Dashboard. No bottom tab bar.
>
> Background: The Security Dashboard screen is visible but covered by a dark overlay (#000000 at 60% opacity).
>
> Modal (centered vertically and horizontally):
> Dark card (#1A3042), border-radius 20px, max-width 320px, padding 32px 24px. No border (the overlay provides contrast).
>
> Inside modal:
> Red circle (60px) with white exclamation mark icon, centered. Below (16px): "Lock Everything?" in Tuka or bold quirky font (24pt, white), centered. Below (12px): "This will immediately freeze all cards, block all transactions, and log out all devices. You can unlock from this screen or by visiting a Maya center." in 14pt #9CA3AF, centered, line-height 1.5.
>
> Buttons (24px below description, stacked, full-width, 12px gap):
> Primary pill: "Yes, Lock My Account" — Red (#FF3B30) solid fill, white text bold, 50px radius, 52px height.
> Secondary pill: "Cancel" — no fill, 1px border #243B4D, white text, 50px radius, 48px height.

---

### Screen 12: Security_Active_Sessions
**Mode:** Text-to-UI

**Stitch Prompt:**
> A real iOS app screen. Active sessions list. Dark background (#112432). No bottom tab bar.
>
> Top: Nav bar on dark. Back chevron white. "Active Sessions" centered bold 17pt white. Line (#243B4D).
>
> Current device card (24px margin, 16px below nav):
> Dark card (#1A3042) with subtle green tint — background linear-gradient(135deg, rgba(117,238,165,0.08), #1A3042). Border 1px #243B4D, border-radius 16px, padding 20px.
> - iPhone icon (white, 20px).
> - "iPhone 15 Pro" bold 16pt white.
> - Row: green dot (6px, #00B463) + "Manila, Philippines · Active now" in 14pt #9CA3AF.
> - Badge pill: "This device" — Maya Green (#75EEA5) fill, #112432 text 12pt bold, 50px radius, padding 4px 12px.
>
> Other sessions (24px margin, 12px below current device):
> Dark grouped list (#1A3042, border 1px #243B4D, 16px radius):
> - Row: Laptop icon (white, 20px) + "MacBook Pro" bold 16pt white + "Manila · 2 hours ago" 14pt #9CA3AF. Right: "Log Out" text in #FF3B30 bold 14pt. Padding 16px 20px.
> - Divider (1px #243B4D, inset 20px).
> - Row: Tablet icon + "iPad Air" bold + "Cebu · 3 days ago" #9CA3AF. Right: "Log Out" in #FF3B30.
>
> Bottom (24px from bottom, 24px margin): Full-width pill "Log Out All Other Devices" — Red (#FF3B30) solid, white text bold, 50px radius, 52px height.

---

## Prototype Connections

| # | Source | Trigger | Destination | Transition |
|---|--------|---------|-------------|------------|
| 1 | Login_Splash | Tap "Unlock with FaceID" | Login_Biometric | Fade (0.3s) |
| 2 | Login_Splash | Tap "Login" | Login_Fallback | Slide right |
| 3 | Login_Biometric | Success | Dashboard (out of scope) | Slide up |
| 4 | Login_Fallback | Tap "Login" | Dashboard (out of scope) | Slide up |
| 5 | Transaction_Pending | Tap amount/details | Transaction_Details | Slide right |
| 6 | Transaction_Details | Status → Complete | Transaction_Complete | Fade (0.3s) |
| 7 | Help_Center_Home | Tap "Ticket #1234" | Help_Ticket_Details | Slide right |
| 8 | Help_Center_Home | Tap "Chat with Support" | Help_Chat_Support | Slide up |
| 9 | Security_Dashboard | Tap Kill Switch | Security_KillSwitch_Confirm | Spring from center |
| 10 | Security_Dashboard | Tap "Active Sessions" | Security_Active_Sessions | Slide right |
| 11 | Security_KillSwitch_Confirm | Tap "Cancel" | Security_Dashboard | Dismiss down |

---

## Refinement Prompts (Dark Mode)

After generating, use these to fix common issues:

- **Background too light:** "Background must be exactly #112432 (Dark Navy), not gray or lighter blue"
- **Cards not dark enough:** "Card backgrounds must be #1A3042, not white or light gray. Borders #243B4D"
- **Text not white:** "All primary text on dark backgrounds must be white #FFFFFF, not black"
- **Green wrong shade:** "Primary buttons must be Maya Green #75EEA5, not a different green"
- **Tab bar appeared:** "Remove the bottom tab bar entirely. This is a detail screen with no app navigation"
- **Pill shape:** "All buttons must be pill-shaped with border-radius 50px"
- **Font:** "Headlines should use a bold quirky font style like Tuka — not a standard thin sans-serif"
- **Dividers too visible:** "Divider lines should be #243B4D (very subtle on dark), not white or light gray"
- **Shield not right:** "The shield should be outlined in Maya Green #75EEA5, not filled solid. Subtle 3D look."

---

## Export Checklist

- [ ] **Figma Export:** Export to Figma → organize by flow (A/B/C/D) → verify dark backgrounds preserved
- [ ] **Code Export:** React + Tailwind CSS → verify dark mode classes used (bg-[#112432] etc.)
- [ ] **Prototype Link:** Generate shareable URL + QR code
- [ ] **Screenshots:** Export all 12 screens as individual PNGs (2x resolution)
- [ ] **Video Walkthrough:** Record all 4 flows (optional)
