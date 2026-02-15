# Stitch Design Assets — Maya Brand

Generate high-quality, interactive prototypes in **Google Stitch** using the prompts below. Each prompt follows **Maya's actual brand language**: clean, minimal, solid white backgrounds, bright mint green CTAs, and generous whitespace.

**Reference:** `screen.png` (login screen) + [maya.ph](https://www.maya.ph) for brand accuracy.

**Workflow:** Use **Sketch-to-UI mode** (wireframe + prompt) for the 4 hero screens, and **Text-to-UI mode** for the 8 supporting screens.

---

## Brand Context (Prefix Every Prompt)

Copy and paste this block at the start of every Stitch prompt:

> **Brand Context:**
> - **Primary Color:** Maya Mint Green (#2FF29E) — bright, fresh mint green for primary CTAs and accents.
> - **Dark Color:** Dark Navy (#112432) — text, icons, dark elements.
> - **Background:** Solid White (#FFFFFF) — clean, no gradients or translucency.
> - **Secondary Colors:** Jade (#00B463) for links/success, Burning Sand (#D69474) for warnings/pending.
> - **Typography:** Headlines in "Cerebri Sans Pro" (bold), Body in "Cerebri Sans Pro" (regular). Clean, geometric sans-serif.
> - **Logo:** Black rounded-square app icon with green "maya" text inside — always centered at top of entry screens.
> - **Button Style:** Full-width pill buttons (border-radius: 50px) with Maya Mint Green gradient, no border. Soft subtle shadow.
> - **Input Style:** Rounded fields (border-radius: 12px) with thin light gray border (#E5E7EB), no fill or very light gray (#F9FAFB).
> - **Layout:** Centered, generous whitespace, clean hierarchy, iOS native feel.
> - **Vibe:** Professional fintech, approachable, trustworthy, clean. Not flashy — confident and simple.

---

## Flow A: Frictionless Login (3 Screens)

### Screen 1: Login_Splash ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `screen.png` (use this as the primary reference — it's the user's preferred design)

**Stitch Prompt:**
> Mobile banking login screen for Maya fintech app, iOS style, matching the reference image exactly.
>
> Background: Solid white (#FFFFFF). Clean, no gradients.
>
> Hero: Centered Maya app icon — black rounded square (120px, border-radius: 28px) with mint green "maya" lowercase wordmark inside. Below it: "Welcome back" in bold (28pt, #000000), centered. Subtitle "Sign in to your account" in regular weight (16pt, #9CA3AF), centered.
>
> FaceID Button: Centered pill-shaped outlined button "Unlock with FaceID" with FaceID smiley icon. Light gray border (#E5E7EB), no fill, rounded (border-radius: 50px), padding 16px 32px. Black text.
>
> Divider: Thin horizontal line with "OR" centered text in gray (#9CA3AF), uppercase, small (12pt).
>
> Input Section: "MOBILE NUMBER" label (12pt, uppercase, #9CA3AF, left-aligned). Below: Full-width input field with placeholder "09XX XXX XXXX" — rounded rectangle (border-radius: 12px), thin gray border (#E5E7EB), light background (#F9FAFB), padding 16px.
>
> Links Row: "Register" in Maya Mint Green (#2FF29E) left-aligned, "Forgot Number?" in gray (#9CA3AF) right-aligned. Both 14pt.
>
> Bottom CTA: Full-width pill button "Login" — Maya Mint Green (#2FF29E) solid background with subtle lighter gradient at center, dark text (#112432), bold (16pt), border-radius: 50px, height: 56px. Pinned to bottom with 24px side margins. Subtle soft shadow (0 4px 12px rgba(47, 242, 158, 0.3)).
>
> Overall: Extremely clean. Lots of whitespace between sections. Centered layout. No decorative elements. Professional fintech feel matching maya.ph aesthetic.

---

### Screen 2: Login_Biometric
**Mode:** Text-to-UI

**Stitch Prompt:**
> Biometric authentication screen for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Center: Large FaceID icon (80px) in Dark Navy (#112432), centered. Below: circular animated indicator ring in Maya Mint Green (#2FF29E), subtle pulse. Below ring: "Verifying your identity..." in regular (16pt, #9CA3AF), centered.
>
> Bottom: Text link "Use password instead" in gray (#9CA3AF), underlined, centered, 14pt.
>
> No navigation bar — this is a full-screen modal state.
>
> Overall: Single focal point. Calming, minimal. White background. No decorative elements.

---

### Screen 3: Login_Fallback
**Mode:** Text-to-UI

**Stitch Prompt:**
> Manual login screen for Maya fintech app, iOS style.
>
> Navigation: Standard iOS back chevron (‹) in Dark Navy (#112432), left-aligned. No title in navbar — clean.
>
> Header: "Login" in bold (28pt, #000000), left-aligned, 24px left margin. Subtitle "Enter your credentials" (16pt, #9CA3AF).
>
> Form (24px horizontal padding, 16px gaps between fields):
> - "MOBILE NUMBER" label (12pt, uppercase, #9CA3AF). Input field: rounded rectangle (12px radius), thin gray border (#E5E7EB), placeholder "+63 9XX XXX XXXX", 16px padding.
> - "PASSWORD" label (12pt, uppercase, #9CA3AF). Input field: same style, lock icon prefix, eye toggle icon on right for show/hide.
> - "Forgot Password?" — text link in Maya Mint Green (#2FF29E), 14pt, right-aligned.
>
> Primary CTA: Full-width pill button "Login" — Maya Mint Green (#2FF29E), dark text (#112432), bold, 50px radius, 56px height. Pinned 24px from bottom.
>
> Divider: "OR" with gray lines.
>
> Secondary CTA: Full-width pill outlined button "Request OTP" — no fill, thin gray border (#E5E7EB), Dark Navy text, 50px radius.
>
> Overall: Clean form layout. Solid backgrounds. Generous spacing. iOS native feel.

---

## Flow B: Transparent Transactions (3 Screens)

### Screen 4: Transaction_Pending ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `transaction_pending_wireframe_hifi_ios.png`

**Stitch Prompt:**
> A real iOS app screen. Transaction pending screen. White background (#FFFFFF). Do NOT add a bottom tab bar. Do NOT add a navigation ribbon with Home, Activity, Scan, Cards, or Profile. The screen has NO bottom navigation at all.
>
> Top: Standard iOS navigation bar. Left: a back arrow (<) in black. Center: "Transaction Pending" in bold 17pt black. A thin 1px line (#F3F4F6) below the nav bar.
>
> Section 1 — Amount (centered, 24px top padding):
> "₱2,500.00" in bold 32pt black, centered. Below it: "Cash In via GCash" in 14pt #9CA3AF, centered. 16px below that: a small pill badge with text "Pending" — background #D69474, white text, 12pt bold, border-radius 50px, padding 4px 12px.
>
> Section 2 — Timer (centered, 24px top gap):
> A simple rounded container (180px wide, 64px tall, border-radius 12px, background #F9FAFB, border 1px #E5E7EB). Inside: the text "2:01" in monospaced font, 36pt bold, color #D69474. Nothing else — no icon, no clock image.
>
> Section 3 — Progress stepper (24px top gap, 24px left padding):
> Row 1: A 24px solid green (#00B463) circle with white checkmark. 12px right: "Request Sent" in 16pt bold black. Below: a vertical 2px green line, 28px tall.
> Row 2: Same green circle with checkmark. "Processing" in 16pt bold black. Below: a vertical 2px line — green top half, light gray (#E5E7EB) bottom half, 28px tall.
> Row 3: A 24px circle, no fill, 2px border #D69474. "Awaiting Confirmation" in 16pt regular, color #6B7280.
>
> Section 4 — Notify toggle (24px top gap):
> A full-width row inside a container with 1px top border #F3F4F6 and 24px horizontal padding, 16px vertical padding. Left: "Notify me when completed" in 16pt black. Right: a standard iOS toggle switch, ON state, green track (#2FF29E), white knob.
>
> Nothing else below this. No tab bar. No bottom navigation. The screen ends with white space after the toggle row. This is a detail screen accessed from a transaction list — it does not have app-level navigation.

---

### Screen 5: Transaction_Details
**Mode:** Text-to-UI

**Stitch Prompt:**
> Transaction details screen for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Navigation: Back chevron + "Transaction Details" centered title (18pt, bold).
>
> Amount Section (centered, 32px top padding):
> - "₱2,500.00" in bold (36pt, #000000).
> - "Cash In via GCash" in regular (14pt, #9CA3AF).
> - Status pill "Processing" — Burning Sand (#D69474) background, white text (12pt, bold), rounded pill (border-radius: 50px), padding 4px 12px.
>
> Details Card (24px margin, white background, light gray border #F3F4F6, 16px radius, 20px padding):
> - Row: "From" (14pt, #9CA3AF) → "GCash Wallet" (16pt, #000000). Right-aligned value.
> - Thin divider (#F3F4F6).
> - Row: "To" → "Maya Savings"
> - Divider.
> - Row: "Reference" → "#MYA-2024-78291" (14pt, #9CA3AF value)
> - Divider.
> - Row: "Date" → "Feb 15, 2026, 2:41 PM"
>
> Mini Progress Bar: Horizontal bar (full width inside card, 4px height, 50px radius). 2/3 filled in green (#00B463), remaining in light gray (#E5E7EB).
>
> Bottom CTA: Full-width pill outlined button "Report an Issue" — no fill, thin gray border, Dark Navy text. 50px radius. 24px from bottom.
>
> Overall: Information-dense but clean. iOS-native grouped list style. Solid colors.

---

### Screen 6: Transaction_Complete
**Mode:** Text-to-UI

**Stitch Prompt:**
> Transaction success screen for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Hero (centered, top 1/3 of screen):
> - Large green circle (80px) with white checkmark icon — solid Jade green (#00B463), no glow or shadow.
> - "Transfer Complete!" in bold (28pt, #000000), centered.
> - "₱2,500.00 received by Maya Savings" in regular (16pt, #9CA3AF), centered.
>
> Receipt Card (24px margin, light gray border #F3F4F6, 16px radius, 20px padding):
> - Row: "Reference" → "#MYA-2024-78291"
> - Divider.
> - Row: "Date" → "Feb 15, 2026, 2:43 PM"
> - Divider.
> - Row: "Fee" → "Free" in green (#00B463)
>
> Toggle Row (inside card or separate): "Send receipt via email" + toggle, Maya Mint Green ON state.
>
> Bottom CTAs (stacked, 12px gap):
> - Primary: Full-width pill "Done" — Maya Mint Green (#2FF29E), Dark Navy text, bold, 50px radius.
> - Text link: "View in Transaction History" — Jade (#00B463), 14pt, centered.
>
> Overall: Positive completion state. Green checkmark is the hero. Clean, celebratory without being flashy.

---

## Flow C: Accessible Support (3 Screens)

### Screen 7: Help_Center_Home ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `help_center_wireframe_hifi_ios.png`

**Stitch Prompt:**
> Help Center home screen for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Navigation: "Help Center" centered title (18pt, bold, #000000). Thin bottom border (#F3F4F6).
>
> My Tickets Section (24px margin):
> - Section label "MY TICKETS" (12pt, uppercase, #9CA3AF, bold).
> - Ticket card: White background, light gray border (#F3F4F6), 16px radius, 20px padding.
>   - "Ticket #1234" in bold (18pt, #000000).
>   - Status pill "Investigating" — Burning Sand (#D69474) background, white text (12pt), pill shape.
>   - "Submitted 2 hours ago" (12pt, #9CA3AF).
>   - Right chevron (›) for navigation.
>
> Top Questions Section:
> - "Top Questions" title (20pt, bold, #000000).
> - iOS-style grouped list — white background, light border, 16px radius:
>   - "How to reset password?" + chevron ›
>   - Thin divider (#F3F4F6)
>   - "View recent transactions" + chevron ›
>   - Divider
>   - "Report lost card" + chevron ›
>   - Divider
>   - "Change contact information" + chevron ›
>   - Divider
>   - "Payment options" + chevron ›
>   Each row: 16pt Dark Navy text, 16px vertical padding, chevron in #9CA3AF.
>
> Bottom CTA: Full-width pill button "Chat with Support" — Dark Navy (#112432) solid background, white text, bold, headset icon left of text, 50px radius, 56px height. 24px from bottom. Subtle shadow.
>
> Overall: Clean iOS-native list style. Accessible, high contrast. Solid backgrounds. No transparency.

---

### Screen 8: Help_Ticket_Details
**Mode:** Text-to-UI

**Stitch Prompt:**
> Support ticket detail screen for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Navigation: Back chevron + "Ticket #1234" centered (18pt, bold).
>
> Status Card (24px margin, light gray border, 16px radius, 20px padding):
> - "Unable to complete cash-in" (18pt, bold, #000000).
> - Status pill "Investigating" — Burning Sand (#D69474) pill, white text.
> - "Priority: High" — small red dot + text (14pt, #6B7280).
>
> Activity Timeline ("Activity" header, 16pt bold):
> Vertical timeline with thin 2px gray left-border line, each entry has:
> - Small circle on the line (8px): green (#00B463) for past, Burning Sand for current.
> - "Ticket Created" — "Feb 15, 2:30 PM" (12pt, #9CA3AF). Description: "You reported: Cash-in from GCash stuck at processing for 30 minutes." (14pt, #000000).
> - "Under Review" — "Feb 15, 2:45 PM". "Agent Maria assigned to your case."
> - "Investigating" (current) — "Feb 15, 3:00 PM". "We're checking with our payment partner." Burning Sand circle.
>
> Bottom CTAs (stacked):
> - Primary pill: "Add a Comment" — Maya Mint Green (#2FF29E), Dark Navy text, full width, 50px radius.
> - Secondary pill: "Call Support" — outlined, gray border, Dark Navy text, phone icon.
>
> Overall: Clear timeline. Simple dots and lines. Solid colors. iOS grouped list aesthetic.

---

### Screen 9: Help_Chat_Support
**Mode:** Text-to-UI

**Stitch Prompt:**
> Live chat support screen for Maya fintech app, iOS style (like iMessage).
>
> Background: Light gray (#F9FAFB) for chat area.
>
> Navigation: Back chevron, "Chat with Maya" (18pt, bold), green online dot (8px, #00B463), "Support Agent" subtitle (12pt, #9CA3AF).
>
> Chat Bubbles:
> - Agent (left-aligned): White bubble (#FFFFFF), rounded (18px radius, bottom-left: 4px), subtle shadow. Text in 14pt Dark Navy. "Hi! I'm here to help. I can see your ticket about the pending cash-in. Let me check the status."
> - Timestamp: "3:05 PM" (10pt, #9CA3AF) below bubble.
> - User (right-aligned): Maya Mint Green (#2FF29E) bubble, rounded (18px radius, bottom-right: 4px). Text in 14pt Dark Navy (#112432). "Thanks! It's been stuck for an hour now."
> - Timestamp: "3:06 PM".
> - Agent: "I've escalated this to our payments team. You should see the funds in 15-30 minutes."
> - Typing indicator: Three gray dots in white bubble, left-aligned.
>
> Quick Replies: Horizontal scroll of pill chips — "Send screenshot", "Check balance", "Escalate to manager" — thin gray border (#E5E7EB), Dark Navy text, 12pt, no fill, 50px radius.
>
> Input Bar: White bar at bottom, thin top border (#F3F4F6). Rounded input field (#F9FAFB background, 50px radius), placeholder "Type a message...", attachment icon (gray), send arrow (Maya Mint Green #2FF29E).
>
> Overall: iMessage-like chat. Clean solid bubbles. Green for user, white for agent. No transparency.

---

## Flow D: Security Center (3 Screens)

### Screen 10: Security_Dashboard ⭐ Hero Screen
**Mode:** Sketch-to-UI
**Input Image:** `security_center_wireframe_hifi_ios.png`

**Stitch Prompt:**
> Security Center dashboard for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Navigation: "Security Center" left-aligned (28pt, bold, #000000), 24px left margin. No back button (this is a main tab).
>
> Hero Shield (centered, 32px top padding):
> - Large shield icon (180px height) — Dark Navy (#112432) fill, clean flat design, not 3D.
> - "80%" in bold (48pt, #000000) centered inside shield.
> - "Secure" in regular (16pt, #000000) below the percentage, inside shield.
> - Small circular loading indicator below shield.
> - Subtext: "Good. 2 actions recommended." (14pt, #9CA3AF), centered.
>
> Kill Switch Card (24px margin, light gray border #F3F4F6, 16px radius, 20px padding):
> - Left section: "Kill Switch" (18pt, bold, #000000). Subtext: "Instantly lock your account." (14pt, #9CA3AF).
> - Right: iOS toggle switch — Red (#FF3B30) track in ON state, white knob. Standard iOS toggle size (51x31px).
>
> Active Sessions Card (same card style):
> - Left: Lock icon (Dark Navy).
> - "Active Sessions" (16pt, bold, #000000).
> - Right: "(3)" count in gray + chevron ›.
>
> Overall: Trustworthy, professional. Shield is dominant visual. Clean cards. Solid colors. iOS native toggles and list styles.

---

### Screen 11: Security_KillSwitch_Confirm
**Mode:** Text-to-UI

**Stitch Prompt:**
> Kill Switch confirmation modal for Maya fintech app, iOS style alert.
>
> Background: Dimmed overlay (black at 40% opacity) over Security Dashboard.
>
> Modal (centered, white #FFFFFF, 20px radius, max-width 320px, 24px padding):
> - Warning icon: Red circle (60px) with white exclamation mark — solid #FF3B30, centered.
> - Title: "Lock Everything?" (24pt, bold, #000000), centered.
> - Description: "This will immediately freeze all cards, block all transactions, and log out all devices. You can unlock from this screen or by visiting a Maya center." (14pt, #6B7280, centered).
>
> Buttons (stacked, full-width, 12px gap):
> - Primary: Pill "Yes, Lock My Account" — Red (#FF3B30) solid, white text, bold, 50px radius.
> - Secondary: Pill "Cancel" — no fill, thin gray border (#E5E7EB), Dark Navy text, 50px radius.
>
> Overall: iOS-style alert. Clean, focused. Red for destructive action. White modal on dark overlay. No fancy effects.

---

### Screen 12: Security_Active_Sessions
**Mode:** Text-to-UI

**Stitch Prompt:**
> Active sessions management screen for Maya fintech app, iOS style.
>
> Background: Solid white (#FFFFFF).
>
> Navigation: Back chevron + "Active Sessions" centered (18pt, bold).
>
> Current Device Card (24px margin, subtle green tint background — #2FF29E at 5% opacity, 16px radius, 20px padding):
> - iPhone icon (Dark Navy, 24px).
> - "iPhone 15 Pro" (16pt, bold, #000000).
> - "Manila, Philippines · Active now" — green dot (#00B463) + text (14pt, #6B7280).
> - "This device" badge — small pill, Maya Mint Green (#2FF29E) background, Dark Navy text (12pt).
>
> Other Sessions (iOS grouped list style, light gray border, 16px radius):
> - Session 1: Laptop icon + "MacBook Pro" (16pt, bold) + "Manila · 2 hours ago" (14pt, gray) + Red text button "Log Out" (#FF3B30, 14pt, right-aligned).
> - Thin divider (#F3F4F6).
> - Session 2: Tablet icon + "iPad Air" + "Cebu · 3 days ago" + Red "Log Out" button.
>
> Bottom CTA: Full-width pill "Log Out All Other Devices" — Red (#FF3B30) solid, white text, bold, 50px radius. 24px from bottom.
>
> Overall: Clean device list. Current session highlighted with subtle green tint. Red for logout actions. iOS grouped list style.

---

## Prototype Connections

After generating all 12 screens, use Stitch's **Prototype mode** to link them:

| # | Source Screen | Trigger | Destination | Transition |
|---|--------------|---------|-------------|------------|
| 1 | Login_Splash | Tap "Unlock with FaceID" | Login_Biometric | Fade (0.3s) |
| 2 | Login_Splash | Tap "Login" | Login_Fallback | Slide right (0.3s) |
| 3 | Login_Biometric | FaceID success (auto) | — (Dashboard, out of scope) | Slide up |
| 4 | Login_Fallback | Tap "Login" button | — (Dashboard) | Slide up |
| 5 | Transaction_Pending | Tap details area | Transaction_Details | Slide right |
| 6 | Transaction_Details | Status → Complete | Transaction_Complete | Fade (0.3s) |
| 7 | Help_Center_Home | Tap "Ticket #1234" | Help_Ticket_Details | Slide right |
| 8 | Help_Center_Home | Tap "Chat with Support" | Help_Chat_Support | Slide up |
| 9 | Security_Dashboard | Tap Kill Switch toggle | Security_KillSwitch_Confirm | Spring from center |
| 10 | Security_Dashboard | Tap "Active Sessions" | Security_Active_Sessions | Slide right |
| 11 | Security_KillSwitch_Confirm | Tap "Cancel" | Security_Dashboard | Dismiss down |

---

## Refinement Prompts

If a screen needs adjustment after generation:

- **Color fix:** "Primary button must be exactly Maya Mint Green #2FF29E, not a darker or blueish green"
- **Pill shape:** "Button border-radius should be 50px — fully pill shaped"
- **More whitespace:** "Add more vertical spacing between sections — at least 24px gaps"
- **Simplify:** "Remove any gradients, shadows, or translucency from card backgrounds — use solid white"
- **Border fix:** "Input borders should be thin light gray #E5E7EB, not dark or thick"
- **Center layout:** "Center the hero section (icon + heading + subtitle) horizontally"
- **iOS native:** "Use standard iOS toggle switch style — not custom"
- **Maya icon:** "App icon should be a black rounded square with green 'maya' text — not a bird or mascot"

---

## Export Checklist

- [ ] **Figma Export:** Click "Export to Figma" → download `.fig` → organize by flow (A/B/C/D)
- [ ] **Code Export:** Select "Export Code" → React + Tailwind CSS → download components
- [ ] **Prototype Link:** Generate shareable URL → create QR code for mobile preview
- [ ] **Screenshots:** Export each of the 12 screens as individual PNGs (2x resolution)
- [ ] **Video Walkthrough:** Record screen recording of all 4 flows (optional)
