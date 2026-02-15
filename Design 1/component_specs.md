# Maya Component Specs v2 — Dark Mode

6 reusable components. Each has a **dark variant** (app screens) and **light variant** (login screens). See `design_tokens.json` for all token values.

---

## 1. Pill Button

### Variants
| Variant | Background | Text | Border | Where |
|---------|-----------|------|--------|-------|
| Primary | #75EEA5 | #112432 | None | Login, Done, Add Comment, Chat with Support |
| Outlined (light) | None | #112432 | 1px #E5E7EB | Request OTP, FaceID button (on white bg) |
| Outlined (dark) | None | #FFFFFF | 1px #243B4D | Report an Issue, Cancel, Call Support (on dark bg) |
| Destructive | #FF3B30 | #FFFFFF | None | Lock Account, Log Out All |

### Specs
```css
.pill-btn {
  width: 100%;
  height: 56px;
  border-radius: 50px;
  font-family: 'Cerebri Sans Pro', system-ui;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  transition: transform 150ms ease-out;
}
.pill-btn:active { transform: scale(0.97); }

/* Primary — works on both light and dark backgrounds */
.pill-btn--primary {
  background: #75EEA5;
  color: #112432;
  box-shadow: 0 4px 12px rgba(117, 238, 165, 0.3);
}

/* Outlined on light (login screens) */
.pill-btn--outlined-light {
  background: none;
  color: #112432;
  border: 1px solid #E5E7EB;
  height: 48px;
}

/* Outlined on dark (app screens) */
.pill-btn--outlined-dark {
  background: none;
  color: #FFFFFF;
  border: 1px solid #243B4D;
  height: 48px;
}

/* Destructive */
.pill-btn--destructive {
  background: #FF3B30;
  color: #FFFFFF;
  height: 52px;
}
```

---

## 2. Card

### Variants
| Variant | Background | Border | Where |
|---------|-----------|--------|-------|
| Dark | #1A3042 | 1px #243B4D | All app screens (Flows B, C, D) |
| Dark highlighted | gradient(rgba(117,238,165,0.08), #1A3042) | 1px #243B4D | Current device, active items |
| Light | #FFFFFF | 1px #F3F4F6 | Login screens (if cards needed) |
| Modal | #1A3042 | None | Kill Switch confirmation |

### Specs
```css
.card {
  border-radius: 16px;
  padding: 20px;
}

.card--dark {
  background: #1A3042;
  border: 1px solid #243B4D;
}

.card--dark-highlighted {
  background: linear-gradient(135deg, rgba(117,238,165,0.08), #1A3042);
  border: 1px solid #243B4D;
}

.card--light {
  background: #FFFFFF;
  border: 1px solid #F3F4F6;
}

.card--modal {
  background: #1A3042;
  border: none;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  padding: 32px 24px;
  max-width: 320px;
}

/* Divider inside dark cards */
.card__divider--dark {
  height: 1px;
  background: #243B4D;
}

/* Divider inside light cards */
.card__divider--light {
  height: 1px;
  background: #F3F4F6;
}
```

---

## 3. Input Field

### Variants
| Variant | Background | Border | Text | Placeholder | Where |
|---------|-----------|--------|------|-------------|-------|
| Light | #F9FAFB | 1px #E5E7EB | #000000 | #9CA3AF | Login screens |
| Dark | #1A3042 | 1px #243B4D | #FFFFFF | #9CA3AF | Chat input, any dark screen forms |

### Specs
```css
.input-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #9CA3AF;
  margin-bottom: 8px;
}

/* Light variant (login) */
.input--light {
  width: 100%;
  height: 52px;
  padding: 16px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  font-size: 16px;
  color: #000000;
}
.input--light:focus {
  border-color: #75EEA5;
}
.input--light::placeholder { color: #9CA3AF; }

/* Dark variant (chat, app screens) */
.input--dark {
  width: 100%;
  height: 44px;
  padding: 12px 16px;
  background: #1A3042;
  border: 1px solid #243B4D;
  border-radius: 50px; /* chat uses pill shape */
  font-size: 14px;
  color: #FFFFFF;
}
.input--dark:focus {
  border-color: #75EEA5;
}
.input--dark::placeholder { color: #9CA3AF; }
```

---

## 4. Progress Stepper

Works on dark backgrounds only (Flows B, C).

### Step States
| State | Circle | Size | Icon | Connector | Label |
|-------|--------|------|------|-----------|-------|
| Completed | Solid #00B463 | 24px | White checkmark | 2px #00B463 | Bold white |
| Active | Solid #D69474 | 24px or 8px | None | 2px #243B4D | Bold white |
| Pending | 2px border #D69474 | 24px | None | 2px #243B4D | Regular #9CA3AF |

### Specs
```css
.stepper { padding: 0 24px; }

.stepper-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  position: relative;
  padding-bottom: 28px;
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
.stepper-circle--completed { background: #00B463; color: #FFFFFF; }
.stepper-circle--active { background: #D69474; color: #FFFFFF; }
.stepper-circle--pending { border: 2px solid #D69474; background: none; }

/* Small circle variant (ticket timeline) */
.stepper-circle--sm {
  width: 8px;
  height: 8px;
}

.stepper-connector {
  position: absolute;
  left: 11px;
  top: 24px;
  width: 2px;
  height: 28px;
}
.stepper-connector--completed { background: #00B463; }
.stepper-connector--pending { background: #243B4D; }
/* Half-and-half connector */
.stepper-connector--transition {
  background: linear-gradient(180deg, #00B463 50%, #243B4D 50%);
}

.stepper-label { font-size: 16px; font-weight: 700; color: #FFFFFF; }
.stepper-label--pending { font-weight: 400; color: #9CA3AF; }
.stepper-timestamp { font-size: 12px; color: #9CA3AF; margin-top: 2px; }
.stepper-description { font-size: 14px; color: #9CA3AF; margin-top: 4px; }
```

---

## 5. Status Pill

Same colors work on both light and dark backgrounds (all have sufficient contrast).

### Variants
| Variant | Background | Text |
|---------|-----------|------|
| Investigating / Processing | #D69474 | #FFFFFF |
| Resolved / Success | #00B463 | #FFFFFF |
| Pending | #9CA3AF | #FFFFFF |
| Critical | #FF3B30 | #FFFFFF |
| Active (device) | #75EEA5 | #112432 |
| Premium (purple) | #6F42C1 | #FFFFFF |

### Specs
```css
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 600;
}

.status-pill--investigating { background: #D69474; color: #FFFFFF; }
.status-pill--success { background: #00B463; color: #FFFFFF; }
.status-pill--pending-state { background: #9CA3AF; color: #FFFFFF; }
.status-pill--critical { background: #FF3B30; color: #FFFFFF; }
.status-pill--active { background: #75EEA5; color: #112432; }
.status-pill--premium { background: #6F42C1; color: #FFFFFF; }
```

---

## 6. Toggle Switch

Standard iOS toggle. Two color variants for the ON state.

### Variants
| Variant | ON track | OFF track | Knob |
|---------|---------|----------|------|
| Default | #75EEA5 (Maya Green) | #243B4D (dark) or #E5E7EB (light) | #FFFFFF |
| Destructive | #FF3B30 (Red) | #243B4D or #E5E7EB | #FFFFFF |

### Specs
```css
.toggle {
  position: relative;
  width: 51px;
  height: 31px;
  border-radius: 50px;
  cursor: pointer;
  transition: background 300ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* OFF states */
.toggle--off-dark { background: #243B4D; }
.toggle--off-light { background: #E5E7EB; }

/* ON states */
.toggle--on-default { background: #75EEA5; }
.toggle--on-destructive { background: #FF3B30; }

.toggle__knob {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 27px;
  height: 27px;
  border-radius: 50%;
  background: #FFFFFF;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
.toggle--on .toggle__knob {
  transform: translateX(20px);
}
```

---

## Component Map

| Screen | Pill Button | Card | Input | Stepper | Status Pill | Toggle |
|--------|-----------|------|-------|---------|-------------|--------|
| 1 Login_Splash | primary, outlined-light | — | light | — | — | — |
| 2 Login_Biometric | — | — | — | — | — | — |
| 3 Login_Fallback | primary, outlined-light | — | light x2 | — | — | — |
| 4 Transaction_Pending | — | dark | — | 3-step | investigating | default |
| 5 Transaction_Details | outlined-dark | dark | — | — | investigating | — |
| 6 Transaction_Complete | primary | dark x2 | — | — | success | default |
| 7 Help_Center_Home | primary | dark x2 | — | — | investigating | — |
| 8 Help_Ticket_Details | primary, outlined-dark | dark | — | timeline | investigating | — |
| 9 Help_Chat_Support | — | — | dark | — | — | — |
| 10 Security_Dashboard | — | dark x2 | — | — | — | destructive |
| 11 Security_KillSwitch | destructive, outlined-dark | modal | — | — | — | — |
| 12 Security_Sessions | destructive | dark, dark-highlighted | — | — | active | — |

---

## Design Principles (v2)

1. **Dark mode is the default** for all app screens. Login/entry stays white.
2. **#75EEA5 is the hero color.** It pops on dark backgrounds. Don't overuse — reserve for CTAs and key accents.
3. **Cards use #1A3042** (not white) on dark backgrounds. Borders are #243B4D (subtle, not harsh).
4. **Tuka for headlines** — bold, quirky, "sleek but cheerful." Cerebri Sans Pro for everything else.
5. **Purple is rare.** Only for premium badges or special features. Don't use it on buttons or backgrounds.
6. **High contrast always.** White text on dark, green buttons on dark — contrast ratio >7:1.
7. **Structural prompts, not vibes.** Specify exact px sizes, hex colors, layout positions. AI tools produce slop from vague descriptions.
