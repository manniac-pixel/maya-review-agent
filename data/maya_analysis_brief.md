# Maya App UX Analysis Brief

---

## PAGE 1: Analysis Summary

### Scope
12,345 user reviews analyzed across Google Play and iOS | August 2025 - February 2026 | Overall sentiment: **mixed-negative**

### Top 5 Critical Issues (Ranked by Priority Score)

| # | Issue | Severity | Frequency | Priority | Business Impact |
|---|-------|----------|-----------|----------|-----------------|
| 1 | **Login & Authentication Failures** | 5/5 | High | 18 | Activation, retention, trust, revenue |
| 2 | **Cash-in Delays** (funds not reflecting for 24h+) | 4/5 | High | 14 | Transaction volume, trust |
| 3 | **Customer Service Unreachable** (dead hotlines, rejected emails) | 5/5 | High | 15 | Trust, revenue |
| 4 | **Unauthorized Transactions** (PHP 9K+ stolen, months to resolve) | 5/5 | High | 15 | Trust, revenue |
| 5 | **Security Concerns** (stolen phone = instant account drain + loan fraud) | 5/5 | High | 15 | Trust, revenue |

### Journey Friction Scores (cumulative — higher = more friction, no upper bound)
- **General flows**: 110.4 (12 pain points -- security, payments, KYC, loans, support)
- **Payments**: 24.0 (cash-in delays + failed transactions)
- **Onboarding**: 23.0 (login failures + duplicate account lockouts)
- **Transfers**: 15.0 (unauthorized transactions)
- **Support**: 15.0 (unreachable customer service)

### Temporal Patterns
- **Persistent (6-7 months):** Payment issues, KYC/onboarding, loan/credit, customer support
- **Emerging (Jan-Feb 2026):** OTP failures, transfer delays, savings problems
- **Improving:** Login issues, cash-in delays showing slight improvement
- **Declining:** Customer service and unauthorized transactions are getting worse

### Version Spike: v2.148.3
45% one-star reviews (vs. 35% baseline) -- driven by login regressions, payment failures, and chatbot-only support. This release caused measurable user trust erosion.

### Competitive Position vs. GCash
Users actively switch to GCash citing: stronger security, better data privacy practices, faster transactions, and functioning customer support. Maya's advantages are limited to interface design preference and some feature breadth.

### What's Working (Preserve These)
- **User-friendly interface** -- consistently praised across all months
- **Easy onboarding** (when it works) -- quick registration and verification
- **Convenient payment options** -- broad bill pay and transfer coverage
- **Savings feature** -- users appreciate interest rates and ease of saving
- **Crypto access** -- small-amount crypto buying valued by users

---

## PAGE 2: Next Steps in the Design Process

### Immediate Actions (Week 1-2)

**1. Login & Authentication Redesign**
- Audit the full login flow: password entry, biometric prompt, OTP delivery, error states
- Map every error message users encounter (users report unclear errors and infinite loops)
- Design a fallback flow: if biometric fails -> password -> email OTP -> support escalation
- Add fingerprint/Face ID as primary login (most-requested feature in Feb 2026)

**2. Security & Trust Sprint**
- Design a "stolen phone" emergency flow: remote lock, freeze transactions, recovery without SIM
- Add transaction confirmation step with biometric approval (user-requested for QR payments)
- Create visible security indicators throughout the app (users need to *feel* safe)

### Short-Term Design Work (Week 3-6)

**3. Payment Flow Fixes**
- Redesign transaction confirmation screen: real-time status updates, not just "Success"
- Add a pending transactions dashboard so users can track funds in transit
- Design retry/cancel flows for stuck transactions

**4. Customer Support Overhaul**
- Replace chatbot-first support with human escalation paths visible in the UI
- Design an in-app ticket tracker (users complain tickets vanish)
- Add contextual help at friction points (login screen, KYC flow, transfer screen)

**5. Error Messaging System**
- Audit and rewrite all error messages to include: what went wrong, why, and what to do next
- Design error states for every screen identified in the friction map (Login, Account Creation, Cash-in, Transfer, Contact Form, Security Settings)

### Medium-Term Design Initiatives (Month 2-3)

**6. KYC/Onboarding Redesign**
- Allow photo upload as alternative to ZOLOZ scanner (top feature request)
- Fix address/birthplace fields (users report Philippine locations missing from dropdowns)
- Design a clear path for minors, OFWs, and users with name changes
- Add progress indicators and save-state so users don't lose progress on crashes

**7. Accessibility & Inclusion**
- Add font size controls (elderly users / "lola" can't read small text)
- Add Tagalog/Filipino language option
- Design for low-bandwidth: reduce image payloads, add offline queuing for transfers
- Test on budget devices (Samsung, Xiaomi, Oppo -- top mentioned brands)

**8. Competitive Feature Parity**
- Design Tap To Pay and Watch Pay features (direct user requests, GCash parity)
- Design biometric approval for third-party QR payments

### Research & Validation

**9. Usability Testing Plan**
- Recruit 3 user segments: first-time users, power users, OFWs
- Test the redesigned login flow, stolen-phone recovery, and payment confirmation
- Test on budget Android devices with slow/intermittent connectivity
- Test with elderly users (font size, navigation clarity)

**10. Metrics to Track Post-Redesign**
- Login success rate (current state: users report 5+ failed attempts)
- Time-to-cash-in-reflection (target: under 5 minutes vs. current 24h+)
- Support ticket resolution time
- 1-star review rate per version (baseline: 35%, target: under 25%)
- App uninstall rate / "switched to GCash" mentions in reviews

---

*Generated from 12,345 reviews | Maya Review Agent Pipeline | February 2026*
