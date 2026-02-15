# Maya Component Specifications

Reusable component library for the Maya app redesign. Clean, minimal, solid design matching maya.ph and the reference `screen.png`.

Reference: `design_tokens.json` for all token values.

---

## 1. Pill Button (Primary CTA)

**Purpose:** Main call-to-action. Maya's signature element — full-width mint green pill.

### Anatomy
```
╭─────────────────────────────────╮
│          Button Label            │  ← Centered text, bold
╰─────────────────────────────────╯
         ↑ Pill shape (50px radius)
         ↓ Soft green shadow
```

### Variants
| Variant | Background | Text | Border | Use Case |
|---------|-----------|------|--------|----------|
| Primary | Maya Mint #2FF29E | Dark Navy #112432 | None | Login, Done, main actions |
| Dark | Dark Navy #112432 | White #FFFFFF | None | Chat with Support, secondary emphasis |
| Outlined | Transparent | Dark Navy #112432 | 1px #E5E7EB | Request OTP, Cancel, tertiary actions |
| Destructive | Red #FF3B30 | White #FFFFFF | None | Lock Account, Log Out All |
| FaceID | Transparent | Black #000000 | 1px #E5E7EB | Unlock with FaceID (with icon) |

### States
| State | Change |
|-------|--------|
| Rest | Default |
| Pressed | scale(0.97) for 150ms |
| Disabled | opacity: 0.4, pointer-events: none |

### CSS
```css
.pill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 56px;
  padding: 0 32px;
  border-radius: 50px;
  font-family: 'Cerebri Sans Pro', system-ui;
  font-size: 16px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: transform 150ms ease-out;
}
.pill-btn:active { transform: scale(0.97); }

.pill-btn--primary {
  background: #2FF29E;
  color: #112432;
  box-shadow: 0 4px 12px rgba(47, 242, 158, 0.3);
}
.pill-btn--dark {
  background: #112432;
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.pill-btn--outlined {
  background: transparent;
  color: #112432;
  border: 1px solid #E5E7EB;
}
.pill-btn--destructive {
  background: #FF3B30;
  color: #FFFFFF;
}
.pill-btn--faceid {
  background: transparent;
  color: #000000;
  border: 1px solid #E5E7EB;
  width: auto;
  padding: 12px 32px;
  height: auto;
}
.pill-btn--disabled {
  opacity: 0.4;
  pointer-events: none;
}
```

### Usage
- **Login_Splash:** "Login" (primary), "Unlock with FaceID" (faceid variant)
- **Login_Fallback:** "Login" (primary), "Request OTP" (outlined)
- **Transaction_Complete:** "Done" (primary)
- **Help_Center_Home:** "Chat with Support" (dark)
- **Help_Ticket_Details:** "Add a Comment" (primary), "Call Support" (outlined)
- **Security_KillSwitch_Confirm:** "Yes, Lock My Account" (destructive), "Cancel" (outlined)
- **Security_Active_Sessions:** "Log Out All Other Devices" (destructive)

---

## 2. Card

**Purpose:** Content container. White background with subtle border. iOS grouped-list style.

### Anatomy
```
┌─────────────────────────────────┐  ← Light gray border (#F3F4F6) or none
│                                 │
│         Content Slot            │  ← 20px padding
│                                 │
└─────────────────────────────────┘  ← 16px border-radius
```

### Variants
| Variant | Background | Border | Shadow | Use Case |
|---------|-----------|--------|--------|----------|
| Default | White #FFFFFF | 1px #F3F4F6 | None | Ticket cards, detail rows, session cards |
| Borderless | White #FFFFFF | None | None | Section containers, inline content |
| Highlighted | #2FF29E at 5% tint | 1px #F3F4F6 | None | Current device, active items |
| Modal | White #FFFFFF | None | modal shadow | Confirmation dialogs |

### CSS
```css
.card {
  background: #FFFFFF;
  border: 1px solid #F3F4F6;
  border-radius: 16px;
  padding: 20px;
}
.card--borderless {
  border: none;
}
.card--highlighted {
  background: rgba(47, 242, 158, 0.05);
}
.card--modal {
  border: none;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

### Divider (inside cards)
```css
.card__divider {
  height: 1px;
  background: #F3F4F6;
  margin: 0 -20px; /* full-bleed within card */
}
```

### Usage
- **All screens:** Primary container for grouped content
- **Transaction_Details:** Receipt rows with dividers
- **Help_Center_Home:** Ticket card, question list group
- **Security_Dashboard:** Kill Switch row, Active Sessions row

---

## 3. Input Field

**Purpose:** Text input matching Maya's clean style — thin border, light background, rounded.

### Anatomy
```
  MOBILE NUMBER                        ← Uppercase label (12pt, #9CA3AF)
┌─────────────────────────────────┐
│  09XX XXX XXXX                   │  ← Placeholder / value
└─────────────────────────────────┘  ← 12px radius, thin gray border
  Register          Forgot Number?    ← Helper links below
```

### States
| State | Border | Background |
|-------|--------|-----------|
| Empty | #E5E7EB | #F9FAFB |
| Focused | #2FF29E (Maya Mint) | #FFFFFF |
| Filled | #E5E7EB | #FFFFFF |
| Error | #FF3B30 | #FFFFFF |

### CSS
```css
.input-label {
  font-size: 12px;
  font-weight: 600;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.input-field {
  width: 100%;
  height: 52px;
  padding: 16px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  font-family: 'Cerebri Sans Pro', system-ui;
  font-size: 16px;
  color: #000000;
  outline: none;
  transition: border-color 200ms ease-out, background 200ms ease-out;
}
.input-field::placeholder {
  color: #9CA3AF;
}
.input-field:focus {
  border-color: #2FF29E;
  background: #FFFFFF;
}
.input-field--error {
  border-color: #FF3B30;
}

.input-helper {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}
.input-helper__link {
  font-size: 14px;
  color: #2FF29E;
  font-weight: 600;
}
.input-helper__link--muted {
  color: #9CA3AF;
  font-weight: 400;
}
```

### Usage
- **Login_Splash:** Mobile number field with Register/Forgot links
- **Login_Fallback:** Mobile number + Password fields
- **Help_Chat_Support:** Chat message input (pill-shaped variant)

---

## 4. Progress Stepper

**Purpose:** Vertical timeline showing status progression. Simple dots and lines — no glass or glow.

### Anatomy
```
  ●─── Request Sent                 ← Green filled circle + checkmark
  │    2:30 PM
  │    ← Solid green connector
  ●─── Processing                   ← Green filled circle + checkmark
  │
  │    ← Connector turns gray
  ○─── Awaiting Confirmation        ← Open circle with colored border
       2:41 PM
```

### Step States
| State | Circle | Size | Icon | Connector |
|-------|--------|------|------|-----------|
| Completed | Solid #00B463 | 24px | White checkmark | 2px solid #00B463 |
| Active | Solid #D69474 | 24px | Animated dot | 2px solid #E5E7EB |
| Pending | Open, 2px border #E5E7EB | 24px | None | 2px solid #E5E7EB |

### CSS
```css
.stepper {
  display: flex;
  flex-direction: column;
  padding: 0 24px;
}
.stepper-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  position: relative;
  padding-bottom: 32px;
}
.stepper-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stepper-circle--completed {
  background: #00B463;
  color: white;
}
.stepper-circle--active {
  background: #D69474;
  color: white;
}
.stepper-circle--pending {
  background: transparent;
  border: 2px solid #E5E7EB;
}
.stepper-connector {
  position: absolute;
  left: 11px; /* center of 24px circle */
  top: 24px;
  width: 2px;
  height: 32px;
}
.stepper-connector--completed {
  background: #00B463;
}
.stepper-connector--pending {
  background: #E5E7EB;
}
.stepper-label {
  font-family: 'Cerebri Sans Pro', system-ui;
  font-size: 16px;
  font-weight: 700;
  color: #000000;
}
.stepper-label--pending {
  color: #6B7280;
  font-weight: 400;
}
.stepper-timestamp {
  font-size: 12px;
  color: #9CA3AF;
  margin-top: 2px;
}
```

### Usage
- **Transaction_Pending:** 3-step vertical timeline
- **Help_Ticket_Details:** Activity timeline with descriptions

---

## 5. Status Pill

**Purpose:** Compact color-coded badge for status indication.

### Anatomy
```
╭───────────────╮
│  ● Investigating │
╰───────────────╯
  ↑ Solid background, rounded pill, white text
```

### Variants
| Variant | Background | Text | Use Case |
|---------|-----------|------|----------|
| Investigating | #D69474 | White | Active support tickets |
| Processing | #D69474 | White | In-progress transactions |
| Resolved | #00B463 | White | Completed tickets |
| Success | #00B463 | White | Completed transactions |
| Pending | #9CA3AF | White | Awaiting action |
| Critical | #FF3B30 | White | Urgent / errors |
| Active | #2FF29E | #112432 | Current session, online |

### CSS
```css
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 50px;
  font-family: 'Cerebri Sans Pro', system-ui;
  font-size: 12px;
  font-weight: 600;
}
.status-pill__dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
.status-pill--investigating,
.status-pill--processing {
  background: #D69474;
  color: #FFFFFF;
}
.status-pill--resolved,
.status-pill--success {
  background: #00B463;
  color: #FFFFFF;
}
.status-pill--pending {
  background: #9CA3AF;
  color: #FFFFFF;
}
.status-pill--critical {
  background: #FF3B30;
  color: #FFFFFF;
}
.status-pill--active {
  background: #2FF29E;
  color: #112432;
}
```

### Usage
- **Help_Center_Home:** "Investigating" on ticket card
- **Transaction_Details:** "Processing" pill
- **Transaction_Complete:** "Success" pill
- **Security_Active_Sessions:** "This device" / "Active now"

---

## 6. Toggle Switch

**Purpose:** iOS-standard toggle. Used for notifications and the Kill Switch.

### Variants
| Variant | ON Color | Description |
|---------|---------|-------------|
| Default | #2FF29E (Maya Mint) | Standard toggles — notifications, receipts |
| Destructive | #FF3B30 (Red) | Kill Switch — critical action |

### States
| State | Track | Knob Position |
|-------|-------|---------------|
| OFF | #E5E7EB (light gray) | Left (2px from edge) |
| ON | Variant color | Right (+20px) |

### CSS
```css
.toggle {
  position: relative;
  width: 51px;
  height: 31px;
  border-radius: 50px;
  background: #E5E7EB;
  cursor: pointer;
  transition: background 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
.toggle--on {
  background: #2FF29E;
}
.toggle--destructive.toggle--on {
  background: #FF3B30;
}
.toggle__knob {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 27px;
  height: 27px;
  border-radius: 50%;
  background: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
.toggle--on .toggle__knob {
  transform: translateX(20px);
}
```

### Kill Switch Specific Behavior
1. User taps toggle → toggle slides ON (red)
2. Confirmation modal appears (Screen 11)
3. "Yes, Lock" → account locked, toggle stays ON
4. "Cancel" → toggle slides back OFF

### Usage
- **Transaction_Pending:** "Notify me when completed" (default variant)
- **Transaction_Complete:** "Send receipt via email" (default)
- **Security_Dashboard:** Kill Switch (destructive variant)

---

## Component Composition Map

| Screen | Pill Button | Card | Input | Stepper | Status Pill | Toggle |
|--------|-----------|------|-------|---------|-------------|--------|
| Login_Splash | primary, faceid | | phone | | | |
| Login_Biometric | | | | | | |
| Login_Fallback | primary, outlined | | phone, password | | | |
| Transaction_Pending | | default | | 3-step | | default |
| Transaction_Details | outlined | default | | | processing | |
| Transaction_Complete | primary | default | | | success | default |
| Help_Center_Home | dark | default | | | investigating | |
| Help_Ticket_Details | primary, outlined | default | | timeline | investigating | |
| Help_Chat_Support | | | chat | | | |
| Security_Dashboard | | default x2 | | | | destructive |
| Security_KillSwitch | destructive, outlined | modal | | | | |
| Security_Sessions | destructive | default, highlighted | | | active | |

---

## Design Principles (from maya.ph + screen.png)

1. **Solid, not transparent.** White backgrounds. No glassmorphism, no blur, no translucency.
2. **Clean borders.** Thin light gray (#E5E7EB or #F3F4F6). Never dark or thick.
3. **Mint green is the hero.** #2FF29E for primary CTAs only. Don't overuse it.
4. **Generous whitespace.** Let content breathe. More space > more decoration.
5. **iOS native patterns.** Grouped lists, standard toggles, back chevrons, centered nav titles.
6. **Flat design.** No shadows except on primary CTA buttons (subtle green shadow). No 3D effects.
7. **Simple typography.** One font family (Cerebri Sans Pro). Bold for emphasis, regular for everything else.
