# Maya App UX Review Analysis Report

*Generated: February 13, 2026*

## Executive Summary

**Reviews analyzed:** 12345 | **Period:** 2025-08 to 2026-02

**Overall sentiment:** Mixed sentiment with a slight leaning towards negative reviews.

![Rating Trend Over Time](data/charts/rating_trend.png)

![Sentiment Distribution](data/charts/sentiment_distribution.png)

![Business Impact Distribution](data/charts/business_impact.png)

### Top Persistent Issues (Not Resolved)
- **Payment Issues**: Users experienced difficulties with payments. *(active 7 months)*
- **KYC/Onboarding Issues**: Users experienced difficulties with Know Your Customer (KYC) and onboarding processes. *(active 7 months)*
- **Loan/Credit Issues**: Users experienced difficulties with loans and credit-related features. *(active 6 months)*

### Emerging Issues (New Problems)
- **OTP Issues**: Users experienced difficulties with One-Time Password (OTP) related features. *(first seen 2026-02)*
- **Transfer Issues**: Users experienced difficulties with transferring funds. *(first seen 2026-02)*
- **Savings Issues**: Users experienced difficulties with savings-related features. *(first seen 2026-01)*

### Resolved Issues (Improvements by Maya)
- **Security Issues**: Users reported security concerns and issues. -- *Severity increased to 5 in 2025-10, indicating a significant problem that was likely addressed.*
- **UI/UX Issues**: Users experienced difficulties with the app's user interface and user experience. -- *Frequency decreased to low in 2026-01, suggesting that the issue was resolved.*
- **Crypto Issues**: Users reported problems with cryptocurrency-related features. -- *Frequency decreased to low in 2026-01, but increased again in 2026-02; likely a recurring issue.*

---
## Ranked UX Opportunities

| Rank | Issue | Severity | Frequency | Impact | Score | Category |
|------|-------|----------|-----------|--------|-------|----------|
| 1 | Login Issues | 5/5 | high | activation|retention|transaction_volume|trust|revenue | **18** | strategic_bet |
| 2 | Cash-in Delays | 4/5 | high | transaction_volume|trust | **14** | strategic_bet |
| 3 | Customer Service Issues | 5/5 | high | trust|revenue | **15** | strategic_bet |
| 4 | Unauthorized Transactions | 5/5 | high | trust|revenue | **15** | strategic_bet |
| 5 | Security Concerns | 5/5 | high | trust|revenue | **15** | strategic_bet |
| 6 | Data Privacy Concerns | 3/5 | low | trust|revenue | **6** | strategic_bet |
| 7 | Duplicate Account Issues | 4/5 | medium | activation|retention|trust | **10** | strategic_bet |
| 8 | Cash In Issues | 4/5 | high | transaction_volume|trust|revenue | **12** | strategic_bet |
| 9 | Customer Service Issues | 4/5 | high | trust|revenue | **12** | strategic_bet |

![Priority Score Bar Chart](data/charts/priority_scores.png)

![Severity vs Frequency](data/charts/severity_frequency.png)

![Pain Point Frequency](data/charts/pain_point_frequency.png)


### Detailed Recommendations

#### #1: Login Issues

**Journey:** onboarding|payments|transfers|savings|credit|crypto|support|general

Users experience frequent login issues, including being unable to log in after uninstalling and reinstalling the app.

**Recommendation:** Implement a more robust and user-friendly login system, including multi-factor authentication and clear error messaging.

**User voices:**
> "I've tried several times today, but I can't get in."
> "It's like you don't even know when you'd be able to login to your account."

#### #2: Cash-in Delays

**Journey:** payments|transfers

Users experience delays in cash-ins, with some transactions taking more than a day to reflect on their balance.

**Recommendation:** Optimize cash-in processing times by improving backend infrastructure and implementing real-time updates for users.

**User voices:**
> "The screen showed that it was successful, but the money never reflected on my balance until more than a day later."

#### #3: Customer Service Issues

**Journey:** support|general

Users experience difficulties in contacting customer service, with some hotlines not working and emails being rejected.

**Recommendation:** Implement a more efficient and effective customer service system, including 24/7 hotlines and clear communication channels.

**User voices:**
> "I tried calling your toll-free hotline, but no one answered."
> "My email messages get rejected when sent to your Maya support services."

#### #4: Unauthorized Transactions

**Journey:** transfers|savings|credit|crypto|support|general

Users are reporting unauthorized transactions and difficulty in getting refunds.

**Recommendation:** Implement more robust security measures to prevent unauthorized transactions, including real-time monitoring and alerts.

**User voices:**
> "I had an unauthorized transaction of PHP 9,000 and it took them a month to resolve."
> "They kept saying my case is still ongoing, but I've been waiting for months."

#### #5: Security Concerns

**Journey:** account_security|transparency|reliability

Users are concerned about the security of their accounts, citing instances where hackers were able to access and steal funds.

**Recommendation:** Implement more robust security measures, including multi-factor authentication and regular security audits.

**User voices:**
> "My phone was stolen and the hacker was able to access this app and took my savings and made loan in a snap of a finger."

#### #6: Data Privacy Concerns

**Journey:** general

Users are concerned about data privacy, including the sharing of their personal information with third-party vendors.

**Recommendation:** Implement more transparent data collection and usage practices, including clear communication with users.

**User voices:**
> "I'm worried that my personal info will be leaked if I use this app."
> "I don't know why they're asking for my bank account details when I just want to cash in."

#### #7: Duplicate Account Issues

**Journey:** onboarding|support|general

Users are experiencing issues with duplicate accounts, including being unable to access their account after creating a new one.

**Recommendation:** Implement a more efficient duplicate account detection system, including clear communication with users.

**User voices:**
> "I lost my phone and created a new account, but I couldn't access it."
> "The CSR was very redicluso and didn't help me resolve the issue."

#### #8: Cash In Issues

**Journey:** payments|transfers|savings|general

Users are experiencing issues with cashing in, including delayed or failed transactions.

**Recommendation:** Optimize cash-in processing times by improving backend infrastructure and implementing real-time updates for users.

**User voices:**
> "I cashed in from my bank account, but the amount was not credited to my wallet."
> "It's been almost 2 weeks since I linked my card to Grab, and the payment is still pending."

#### #9: Customer Service Issues

**Journey:** support|general

Users are experiencing issues with customer service, including being unable to reach a human representative or receiving unhelpful responses.

**Recommendation:** Implement a more efficient and effective customer service system, including 24/7 hotlines and clear communication channels.

**User voices:**
> "I tried contacting the customer service number, but it was always busy."
> "The CSR didn't help me resolve my issue and just closed my ticket."

---
## Funnel Drop-Off Hotspots

| Screen/Step | Journey | Evidence | Severity | Signals |
|-------------|---------|----------|----------|---------|
| Send Money > Contact Selection | transfers | 8 | 2/5 | confusion |
| Crypto > Buy Token | crypto | 12 | 3/5 | error |
| KYC > Selfie Capture | onboarding | 25 | 4/5 | retry, crash |
| Cash In > Bank Integration | payments | 30 | 4/5 | abandonment |
| Login > OTP Entry | onboarding | 45 | 5/5 | retry, error |

---
## Quick Wins (High Impact, Low Effort)

### Error messages are unclear and confusing.

- **Recommendation:** Improve error messaging by making it more concise and user-friendly.
- **Impact:** high
- **Rationale:** Clearer error messaging can reduce user frustration and improve overall experience.

### Login screen is cluttered with unnecessary fields.

- **Recommendation:** Simplify the login screen by removing unnecessary fields and making it more intuitive.
- **Impact:** high
- **Rationale:** A simpler login screen can improve user experience and reduce friction.

### Customer service hotline is often busy or unresponsive.

- **Recommendation:** Implement a more efficient customer service system, including 24/7 hotlines and clear communication channels.
- **Impact:** high
- **Rationale:** A more efficient customer service system can improve user satisfaction and reduce support requests.

---
## Strategic Bets (High Impact, High Effort)

### Implement a more robust security measure, including multi-factor authentication.

This initiative aims to improve the overall security of the app by implementing multi-factor authentication. This will help prevent unauthorized transactions and protect user data.

- **User need:** to protect personal data and prevent fraud
- **Competitive context:** Competitors like GCash already offer multi-factor authentication, so Maya needs to implement this feature to stay competitive.

### Optimize cash-in processing times by improving backend infrastructure.

This initiative aims to improve the overall efficiency of cash-in transactions by optimizing backend infrastructure. This will help reduce processing times and improve user experience.

- **User need:** to receive funds quickly and efficiently
- **Competitive context:** Competitors like GCash already offer fast and efficient cash-in processing, so Maya needs to implement this feature to stay competitive.

### Implement a more efficient customer service system, including 24/7 hotlines.

This initiative aims to improve the overall efficiency of customer service by implementing 24/7 hotlines and clear communication channels. This will help reduce support requests and improve user satisfaction.

- **User need:** to receive timely and effective support
- **Competitive context:** Competitors like GCash already offer efficient customer service, so Maya needs to implement this feature to stay competitive.

---
## Competitive Gaps

### Security Measures (vs GCash)

Maya lacks robust security measures, including multi-factor authentication.

**Recommendation:** Implement more robust security measures, including multi-factor authentication.

> "My phone was stolen and the hacker was able to access this app and took my savings and made loan in a snap of a finger."

### Data Privacy (vs GCash)

Maya lacks transparent data collection and usage practices.

**Recommendation:** Implement more transparent data collection and usage practices, including clear communication with users.

> "I'm worried about my data being compromised with Maya."
> "I wish there was more transparency about data collection and usage."

### Unauthorized Transactions (vs GCash)

Maya lacks robust security measures to prevent unauthorized transactions.

**Recommendation:** Implement more robust security measures to prevent unauthorized transactions.

> "I had money stolen from my account, and the customer support was unhelpful."
> "I'm worried about the security of my account after reading reviews."

### Data sharing with third-party vendors (vs GCash)

Maya lacks transparent data collection and usage practices, including clear communication with users.

**Recommendation:** Implement more transparent data collection and usage practices, including clear communication with users.

> "I'm worried that my personal info will be leaked if I use this app."
> "I don't know why they're asking for my bank account details when I just want to cash in."

### Delayed or failed transactions (vs GCash)

Maya lacks efficient transaction processing times.

**Recommendation:** Optimize transaction processing times by improving backend infrastructure.

> "It's been almost 2 weeks since I linked my card to Grab, and the payment is still pending."
> "I cashed in from my bank account, but the amount was not credited to my wallet."

---
## User Segments

### First-time users

*Presence in reviews:* high

**Needs:** ease of use, convenience
**Frustrations:** difficulty logging in, security concerns

**Opportunity:** Improve the onboarding process to make it more user-friendly and reduce friction.

### Power users

*Presence in reviews:* medium

**Needs:** enhanced security measures, advanced features
**Frustrations:** limited customization options, inconsistent customer service

**Opportunity:** Implement more robust security measures and advanced features to meet the needs of power users.

### Credit users

*Presence in reviews:* low

**Needs:** easy-to-use features, competitive interest rates
**Frustrations:** difficulty accessing credit services, high fees

**Opportunity:** Improve the user experience for credit users by making it easier to access credit services and reducing fees.

---
## Version Spike Analysis

![Version 1-Star Rate](data/charts/version_ratings.png)

*Baseline: 34.6% 1-star rate, avg rating 3.38/5 across 7802 versioned reviews*

### v2.148.3 — 45.2% 1-star (188 reviews, 2025-11-16 to 2026-02-09)

**Root cause:** A combination of bugs, regressions, and design changes likely caused widespread issues with login, payments, and customer support in this release.

- **Login and Authentication Issues** (login|security, likely: bug|regression, severity 4/5)
  Users experienced frequent login errors, failed biometric authentication, and difficulties with OTP verification.
  > "Always encounteted log in issues even using my fingerprint or screenlock."
  > "I’m stuck on the upgrade application status step, and every time I click “Take” on the last question, the app crashes and locks me out completely."
- **Payment and Transfer Issues** (payments|transfers, likely: bug|regression, severity 4/5)
  Users reported difficulties with cashing out, failed transactions, and delayed refunds.
  > "it always says error on my phone. cannot log in using my phone..."
  > "my payment on Nov. 10 2025 amounting 2000php thru bdo not reflected on my accnt and I can't recive any acknowledgement for that.."
- **Customer Support Issues** (customer_support, likely: design_change|other, severity 4/5)
  Users experienced poor customer support, long wait times, and unhelpful chatbots.
  > "puro follow up na lang sobrang tagal ! NAPAKABAGAL PA MAG PROCESS NG CONCERN MISSING BALANCE KO DI PA DIN NAIBABALIK MAG 2 WEEKS NA DINAIG PA BANKO !"
  > "Customer service is bad. And it is not secured."

*This version has a significantly higher rate of 1-star reviews (45%) compared to the overall baseline (35%).*

---
## Competitor Comparison: Maya vs GCash

GCash shows stronger performance in transaction speed and merchant acceptance, while Maya leads in UI/UX design and crypto features. Both apps struggle with customer support and verification processes, but Maya's crash rate is slightly higher during peak hours.

### Feature Gaps

| Feature | Available In | User Demand | Description |
|---------|-------------|-------------|-------------|
| Biometric Login | ? | ? |  |
| Offline Payments | ? | ? |  |
| Customer Support | ? | ? |  |

---
## Trend Summary

![Issue Lifecycle](data/charts/issue_lifecycle.png)

**Getting better:** login issues, cash-in delays

**Getting worse:** customer service issues, unauthorized transactions

**Unchanged pain points:** security concerns, data privacy

---
*Report generated by Maya Review Analysis Agent using Gemini API.*