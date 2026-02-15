# Maya App UX Research Hub

## Overview

| Field | Value |
|---|---|
| **Total Reviews Analyzed** | 12,345 |
| **Date Range** | August 2025 — February 2026 |
| **Platforms** | Google Play (primary), iOS |
| **Overall Sentiment** | Mixed-negative |
| **Pipeline Version** | Maya Review Agent v2 (Enhanced) |

---

## 1. Executive Summary

### Sentiment Snapshot

The Maya app has a **mixed-negative sentiment** across 12,345 reviews over 7 months. While users appreciate the interface design and feature breadth, critical issues around login reliability, transaction security, and customer support are driving users to competitors (primarily GCash).

### Key Numbers

| Metric | Value |
|---|---|
| Average Rating | ~3.4 / 5 |
| 1-Star Review Rate | 35% baseline |
| Worst Version (v2.148.3) | 45% 1-star |
| Persistent Issues (6-7 months) | 4 |
| Emerging Issues (Jan-Feb 2026) | 3 |

---

## 2. Top Critical Issues (Ranked)

### #1 — Login & Authentication Failures

| Field | Detail |
|---|---|
| **Severity** | 5/5 |
| **Frequency** | High |
| **Priority Score** | 18 |
| **Business Impact** | Activation, retention, trust, revenue |
| **Affected Journeys** | Onboarding, payments, transfers, savings, credit, crypto, support |
| **Trend** | Improving (slightly) |

**User Quotes:**
> "I've tried several times today, but I can't get in."

> "It's like you don't even know when you'd be able to login to your account."

**Recommendation:** Implement a more robust login system with multi-factor authentication, biometric primary login, and clear error messaging with recovery paths.

---

### #2 — Cash-in Delays

| Field | Detail |
|---|---|
| **Severity** | 4/5 |
| **Frequency** | High |
| **Priority Score** | 14 |
| **Business Impact** | Transaction volume, trust |
| **Affected Journeys** | Payments, transfers |
| **Trend** | Improving (slightly) |

**User Quotes:**
> "The screen showed that it was successful, but the money never reflected on my balance until more than a day later."

**Recommendation:** Optimize cash-in processing. Add real-time status updates and a pending transactions dashboard.

---

### #3 — Customer Service Unreachable

| Field | Detail |
|---|---|
| **Severity** | 5/5 |
| **Frequency** | High |
| **Priority Score** | 15 |
| **Business Impact** | Trust, revenue |
| **Affected Journeys** | Support, general |
| **Trend** | Declining (getting worse) |

**User Quotes:**
> "I tried calling your toll-free hotline, but no one answered."

> "My email messages get rejected when sent to your Maya support services."

**Recommendation:** Implement 24/7 hotlines, human escalation paths visible in UI, and an in-app ticket tracker.

---

### #4 — Unauthorized Transactions

| Field | Detail |
|---|---|
| **Severity** | 5/5 |
| **Frequency** | High |
| **Priority Score** | 15 |
| **Business Impact** | Trust, revenue |
| **Affected Journeys** | Transfers, savings, credit, crypto, support |
| **Trend** | Declining (getting worse) |

**User Quotes:**
> "I had an unauthorized transaction of PHP 9,000 and it took them a month to resolve."

> "They kept saying my case is still ongoing, but I've been waiting for months."

**Recommendation:** Real-time transaction monitoring and alerts. Biometric confirmation for all outgoing transactions.

---

### #5 — Security Concerns

| Field | Detail |
|---|---|
| **Severity** | 5/5 |
| **Frequency** | High |
| **Priority Score** | 15 |
| **Business Impact** | Trust, revenue |
| **Affected Journeys** | Account security, transparency, reliability |
| **Trend** | Stable |

**User Quotes:**
> "My phone was stolen and the hacker was able to access this app and took my savings and made loan in a snap of a finger."

**Recommendation:** Design a stolen-phone emergency flow: remote lock, freeze transactions, recovery without SIM.

---

### #6 — Data Privacy Concerns

| Field | Detail |
|---|---|
| **Severity** | 3/5 |
| **Frequency** | Low |
| **Priority Score** | 6 |
| **Business Impact** | Trust, revenue |

---

### #7 — Duplicate Account Issues

| Field | Detail |
|---|---|
| **Severity** | 4/5 |
| **Frequency** | Medium |
| **Priority Score** | 10 |
| **Business Impact** | Activation, retention, trust |

---

### #8 — Cash-In Transaction Failures

| Field | Detail |
|---|---|
| **Severity** | 4/5 |
| **Frequency** | High |
| **Priority Score** | 12 |
| **Business Impact** | Transaction volume, trust, revenue |

---

### #9 — Customer Service Quality

| Field | Detail |
|---|---|
| **Severity** | 4/5 |
| **Frequency** | High |
| **Priority Score** | 12 |
| **Business Impact** | Trust, revenue |

---

## 3. Journey Friction Map

> Friction scores are cumulative weighted values (higher = more friction, no upper bound). They aggregate the number of pain points multiplied by their severity.

| Journey | Friction Score | Pain Points | Top Issues |
|---|---|---|---|
| **General** | 110.4 | 12 | Security, Payments, KYC, Loans, Support |
| **Payments** | 24.0 | 2 | Cash-in Delays, Cash-In Failures |
| **Onboarding** | 23.0 | 2 | Login Failures, Duplicate Account Lockouts |
| **Transfers** | 15.0 | 1 | Unauthorized Transactions |
| **Support** | 15.0 | 1 | Unreachable Customer Service |

---

## 4. Screen-Level Friction Map

### Critical Priority

| Screen | Journey | Severity | Issue | Recommendation |
|---|---|---|---|---|
| **Login Screen** | Onboarding | 5/5 | Users unable to log in due to technical difficulties | Implement robust login with multiple auth methods |
| **Transfer — Recipient Selection** | Transfers | 5/5 | Unauthorized transactions occurring | Improve recipient selection and verification |
| **Support — Contact Us Form** | Support | 5/5 | Users can't contact support through the form | Improve form + provide effective communication channels |

### High Priority

| Screen | Journey | Severity | Issue | Recommendation |
|---|---|---|---|---|
| **Account Creation / Verification** | Onboarding | 4/5 | Duplicate accounts, verification failures | Prevent duplicate accounts, improve verification |
| **Cash In — Bank Account Selection** | Payments | 4/5 | Problems linking bank accounts for cash-ins | Simplify bank linking, improve error handling |
| **Transaction Confirmation** | Payments | 4/5 | Delays in receiving confirmation | Improve processing times, clearer confirmation |
| **Security Settings** | General | 5/5 | Issues accessing/managing security settings | Improve settings UI and protection |
| **Payment History** | General | 4/5 | Problems viewing/managing payment history | Simplify history, better error handling |

---

## 5. Flow Sequences

### Onboarding Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Login Screen | Auth failures, biometric not prompting, OTP delays | HIGH |
| 2 | Account Creation / Verification | Duplicate accounts, KYC scanner fails, missing locations | HIGH |

### Payments Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Cash In — Bank Account Selection | Bank linking errors | MEDIUM |
| 2 | Transaction Confirmation | Funds not reflecting for 24h+ | HIGH |

### Transfers Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Transfer — Recipient Selection | Unauthorized transactions | CRITICAL |

### Support Flow

| Step | Screen | Known Issues | Drop-off Risk |
|---|---|---|---|
| 1 | Support — Contact Us Form | Form doesn't work, tickets vanish | CRITICAL |

---

## 6. Competitive Analysis

### vs. GCash

| Dimension | Maya | GCash | Gap |
|---|---|---|---|
| **Security** | Weak (stolen phone = instant drain) | Multi-factor auth | Maya needs MFA |
| **Data Privacy** | Low transparency | Better practices | Maya needs clear privacy policy |
| **Transaction Speed** | Cash-in delays (24h+) | Fast processing | Maya needs backend optimization |
| **Customer Support** | Dead hotlines, rejected emails | More responsive | Maya needs 24/7 support |
| **UI Design** | Users prefer Maya's design | Functional but less polished | Maya advantage — preserve this |
| **Features** | Broader (crypto, savings, loans) | More payment integrations | Mixed |

**Key risk:** Users actively switching to GCash citing reliability and security.

---

## 7. Temporal Trends

### Persistent Issues (6-7 months active)

| Issue | Active Since | Severity | Frequency |
|---|---|---|---|
| Payment Issues | Aug 2025 | 4/5 | High |
| KYC/Onboarding | Aug 2025 | 4/5 | High |
| Loan/Credit Issues | Sep 2025 | 4/5 | High |
| Customer Support | Aug 2025 | 4/5 | High |

### Emerging Issues (first seen recently)

| Issue | First Seen | Severity |
|---|---|---|
| OTP Failures | Feb 2026 | 4/5 |
| Transfer Delays | Feb 2026 | 4/5 |
| Savings Issues | Jan 2026 | 3/5 |

### Trend Direction

| Trend | Issues |
|---|---|
| Improving | Login issues, cash-in delays |
| Declining | Customer service, unauthorized transactions |
| Stable | Security concerns, data privacy |

---

## 8. Version Spike Analysis

### v2.148.3 — Regression Release

| Metric | Value |
|---|---|
| **Reviews** | 188 |
| **Average Rating** | 2.95 / 5 |
| **1-Star Rate** | 45.2% (vs. 35% baseline) |
| **Date Range** | Nov 16, 2025 — Feb 9, 2026 |

**Root Cause:** Combination of bugs, regressions, and design changes causing widespread login, payment, and support failures.

| Category | Issues | Type |
|---|---|---|
| Login & Auth | Failed biometric, OTP failures, login loops | Bug / Regression |
| Payments & Transfers | Cash-out errors, failed transactions, delayed refunds | Bug / Regression |
| Customer Support | Chatbot-only, long waits, unhelpful responses | Design Change |

### All Versions (by 1-star rate)

| Version | Reviews | Avg Rating | 1-Star Rate | Status |
|---|---|---|---|---|
| v2.148.3 | 188 | 2.95 | 45.2% | SPIKE |
| v2.151.0 | 258 | 3.13 | 42.2% | |
| v2.147.1 | 679 | 3.30 | 36.8% | |
| v2.151.1 | 1,430 | 3.37 | 35.6% | |
| v2.145.0 | 582 | 3.34 | 35.1% | |
| v2.152.0 | 429 | 3.40 | 33.6% | |
| v2.146.0 | 665 | 3.40 | 33.2% | |
| v2.141.1 | 86 | 4.24 | 16.3% | Best |

---

## 9. Positive Signals (Preserve These)

| Signal | Frequency | Context |
|---|---|---|
| **User-friendly interface** | High | Consistently praised, preferred over GCash design |
| **Easy onboarding** (when working) | High | Quick registration and verification |
| **Convenient payment options** | Medium | Broad bill pay and transfer coverage |
| **Savings feature** | Medium | Interest rates and goal-based saving appreciated |
| **Crypto access** | Medium | Small-amount crypto buying valued |
| **Security perception** (by satisfied users) | Medium | OTP double-verification seen as positive |

---

## 10. Feature Requests (User-Driven)

### High Priority

- [ ] Tap To Pay (GCash parity)
- [ ] Watch Pay (GCash parity)
- [ ] Biometric approval for QR payments with 3rd party vendors
- [ ] Fingerprint login as primary option
- [ ] Email OTP / 2FA via authenticator app
- [ ] Photo upload alternative for KYC (ZOLOZ scanner fails)
- [ ] Improved customer support (human agents, faster response)

### Medium Priority

- [ ] Higher credit limits
- [ ] Personal loan feature expansion
- [ ] Enhanced crypto trading features
- [ ] Simplified KYC process

### Low Priority

- [ ] Night mode / dark theme
- [ ] QR code payment feature
- [ ] Enhanced savings features (higher interest, flexible withdrawal)

---

## 11. User Segments

| Segment | Priority | Needs | Frustrations |
|---|---|---|---|
| **First-time users** | High | Ease of use, convenience | Login failures, security concerns |
| **Power users** | Medium | Enhanced security, advanced features | Limited customization, inconsistent support |
| **Credit users** | Low | Easy features, competitive rates | Difficulty accessing credit, high fees |

---

## 12. App Store Screenshots (Captured)

### Available Screenshots (Google Play)

| # | Screen | Covers Friction Point? |
|---|---|---|
| 01 | Wallet / Home Dashboard | Partially (Cash In entry) |
| 02 | Maya Black Credit Card promo | No |
| 03 | Credit Card Management | No |
| 04 | Credit Card Approval | No |
| 05 | Credit Card Freeze/Unfreeze | Partially (security) |
| 06 | Savings Screen | No |
| 07 | Personal Loan Screen | No |

> **Note:** Store screenshots are marketing images showing happy-path flows only. They do not cover the critical friction screens identified in the review analysis.

### Missing Friction Screens — Manual Capture Needed

- [ ] **Login Screen** — capture login form, biometric prompt, error states, OTP entry
- [ ] **Account Creation / KYC Flow** — capture each step: phone entry, ID upload, selfie, ZOLOZ scanner, address fields, error states
- [ ] **Cash In Flow** — capture bank selection, amount entry, confirmation, pending state, success/failure states
- [ ] **Transaction Confirmation** — capture the confirmation screen, "successful" message, pending state
- [ ] **Transfer — Recipient Selection** — capture recipient search, contact selection, amount entry, confirmation
- [ ] **Support — Contact Us Form** — capture help center, form fields, chatbot interface, escalation options
- [ ] **Security Settings** — capture settings screen, biometric toggle, password change, 2FA options
- [ ] **Payment History** — capture transaction list, detail view, filter options

---

## 13. Screen Capture Checklist

### Login & Authentication Flow
- [ ] App launch / splash screen
- [ ] Login screen (phone number / email entry)
- [ ] Password entry screen
- [ ] Biometric authentication prompt (fingerprint / Face ID)
- [ ] OTP entry screen
- [ ] OTP not received state
- [ ] Login error message (each unique error)
- [ ] "Security measures" lockout screen
- [ ] Forgot password flow (each step)
- [ ] Account recovery flow

### KYC / Onboarding Flow
- [ ] Registration — phone number entry
- [ ] Registration — personal info form
- [ ] Registration — address entry (capture the dropdown with missing locations)
- [ ] ID selection screen
- [ ] ID photo capture / upload
- [ ] ZOLOZ selfie scanner
- [ ] ZOLOZ failure / retry state
- [ ] Verification pending screen
- [ ] Verification success / failure
- [ ] Account upgrade prompt

### Cash-In Flow
- [ ] Cash-in method selection (bank, 7-Eleven, etc.)
- [ ] Bank account selection / linking
- [ ] Amount entry
- [ ] Confirmation screen (before submit)
- [ ] Processing / loading state
- [ ] Success screen
- [ ] "Pending" or delayed state
- [ ] Failure / error screen

### Transfer Flow
- [ ] Transfer type selection
- [ ] Recipient selection / search
- [ ] Recipient details confirmation
- [ ] Amount entry
- [ ] Transaction confirmation (before submit)
- [ ] Biometric / password confirmation
- [ ] Success screen
- [ ] Failure / error screen

### Support Flow
- [ ] Help center home
- [ ] FAQ / article view
- [ ] Contact us form
- [ ] Chatbot interface
- [ ] Ticket submission confirmation
- [ ] Ticket status / tracker (if exists)
- [ ] Phone support option screen

### Security & Settings
- [ ] Settings main screen
- [ ] Security settings
- [ ] Biometric toggle
- [ ] Password change flow
- [ ] PIN change flow
- [ ] Card freeze/unfreeze
- [ ] Active sessions / device management
- [ ] Data privacy settings

---

## 14. Design Process — Next Steps

### Phase 1: Immediate (Week 1-2)

- [ ] **Login & Auth Redesign** — Audit full login flow, map every error message, design fallback chain (biometric -> password -> email OTP -> support), add fingerprint as primary login
- [ ] **Security & Trust Sprint** — Design stolen-phone emergency flow (remote lock, freeze, SIM-less recovery), add biometric transaction approval, create visible security indicators

### Phase 2: Short-Term (Week 3-6)

- [ ] **Payment Flow Fixes** — Redesign transaction confirmation with real-time status, add pending transactions dashboard, design retry/cancel flows for stuck transactions
- [ ] **Customer Support Overhaul** — Replace chatbot-first with human escalation paths, design in-app ticket tracker, add contextual help at friction points
- [ ] **Error Messaging System** — Audit and rewrite all error messages (what went wrong + why + what to do next), design error states for every friction screen

### Phase 3: Medium-Term (Month 2-3)

- [ ] **KYC/Onboarding Redesign** — Photo upload alternative to ZOLOZ, fix address/birthplace dropdowns, design paths for minors/OFWs/name changes, add progress indicators with save-state
- [ ] **Accessibility & Inclusion** — Font size controls, Tagalog/Filipino language, low-bandwidth optimization, budget device testing (Samsung, Xiaomi, Oppo)
- [ ] **Competitive Feature Parity** — Design Tap To Pay, Watch Pay, biometric QR payment approval

### Phase 4: Validation

- [ ] **Usability Testing** — Recruit 3 segments (first-time users, power users, OFWs), test redesigned login, stolen-phone recovery, payment confirmation, test on budget Android + slow connectivity, test with elderly users
- [ ] **Success Metrics** — Login success rate (target: >95%), time-to-cash-in-reflection (target: <5 min), support resolution time, 1-star rate per version (target: <25%), "switched to GCash" mention reduction

---

## 15. Monthly Breakdown

### August 2025

**Pain Points:** Login (4/5), Payments (4/5), Customer Support (4/5), KYC (4/5), Loans (3/5), Security (3/5), Performance (3/5)
**Feature Requests:** Email OTP/2FA (high), Improved Support (high), Simplified KYC (medium), Faster Loan Approval (medium)
**Positive:** Convenience (high), Security perception (medium)

### September 2025

**Pain Points:** Payments (4/5), Loans (4/5), KYC (3/5), Support (3/5), Security (2/5)
**Feature Requests:** Crypto Support (high), Personal Loan (medium)
**Positive:** Convenience/Ease of Use (high), Security/Trust (medium)

### October 2025

**Pain Points:** Login (4/5), Loans (4/5), Support (4/5), Security (5/5), KYC (3/5), UI/UX (3/5), Performance (3/5)
**Feature Requests:** Night Mode (low), QR Code Payment (low)
**Positive:** Convenience (high), Security (medium)

### November 2025

**Pain Points:** Payments (4/5), Loans (4/5), KYC (3/5), Support (3/5), Security (3/5), UI/UX (2/5)
**Feature Requests:** Photo ID Upload (high), Improved Loan Process (high), Better Support (medium)
**Positive:** Convenience (high), Security (medium)

### December 2025

**Pain Points:** Payments (4/5), Loans (4/5), Support (4/5), KYC (3/5), Crypto (3/5)
**Feature Requests:** Higher Credit Limits (high), Better Support (high), Enhanced Crypto (medium)
**Positive:** Convenience/Ease of Use (high), Security (medium)

### January 2026

**Pain Points:** Support (4/5), Payments (4/5), KYC (3/5), Loans (3/5), Savings (2/5), Crypto (2/5), UI/UX (2/5), Security (2/5)
**Feature Requests:** Improved Support (high), Enhanced Payments (high), Simplified KYC (medium), Better Loans (medium), Savings Features (low), Crypto Trading (low), Better UI (low), Security Features (low)
**Positive:** User-Friendly Interface (high), Convenience (high), Security (medium)

### February 2026

**Pain Points:** Login (4/5), OTP (4/5), Transfers (4/5), Loans (4/5), Crypto (4/5), Support (4/5), Security (4/5), KYC (3/5), Savings (3/5), UI/UX (3/5), Performance (3/5), Onboarding (3/5)
**Feature Requests:** Tap To Pay (high), Watch Pay (high), Biometric Approval (high), Fingerprint Login (high)
**Positive:** Easy to Use (high), Convenient (high), Reliable (high)

---

*Generated from 12,345 reviews | Maya Review Agent Pipeline | February 2026*
