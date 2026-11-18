# Member 1 - two-minute presentation

## Speaking script

**0:00-0:20 - introduce scope**

“We are Group 7. We selected WooCommerce, and our project covers API testing, manual system testing, automated UI testing and performance testing. My scenario checks a purchase across the staff and guest sides.”

**0:20-0:50 - show setup and purchase**

“I created our own product, G07 ST01 TestMug, at 199 baht with ten units in stock. In a separate Incognito guest session, I added one unit and checked the cart total. The order confirmation shows order 807, one mug, 199 baht and cash on delivery.”

Show original product/cart/confirmation screenshots.

**0:50-1:15 - explain unusual actions and inputs**

“I also checked two non-normal paths. Going back from checkout preserved one mug and the correct total. Leaving First name blank showed ‘Please enter a valid first name’. The original run had evidence gaps, so these were repeated and captured as separately dated follow-up checks.”

Show follow-up screenshots 01 and 02. For the live manual demo, show one of these checks; keep valid checkout submission out of this short demonstration so you do not create an unnecessary order.

**1:15-1:40 - verify both sides**

“Staff saw the same order and total. The stock note showed ten reduced to nine. After I saved Completed, the guest confirmation also showed ‘Order completed’ with the same order and total.”

Show original staff Completed screenshot and follow-up guest Completed screenshot.

**1:40-2:00 - finding and handoff**

“The purchase and stock checks passed. We also observed email-send failures in the staff notes, which may be a lab mail-configuration issue. I prepared a repeatable Selenium test with fresh data, but its fresh browser was blocked before login in my execution environment, so I have not claimed two passing automated runs. Sun will explain our API testing next.”

Replace the automation sentence only after two actual full passing runs have been saved. The group still needs a working live UI demo for its presentation; coordinate that with Member 3. Do not present the blocked execution as a passing test.

## Likely questions

- **Why is this system testing?** It verifies a complete staff-to-guest-to-staff process and cross-checks order data, stock and customer-visible completion.
- **Why use G07 names and fictional data?** The server is shared; the data must be recognizable as ours and avoid real personal information.
- **Why guest checkout?** That is the flow actually executed. The guest confirmation is verified; My Account behavior is not claimed.
- **Why test again after going back?** It checks that navigation preserves cart state and does not duplicate or lose the item.
- **Was email failure a product bug?** We observed the failure, but have not established its root cause. The message points to a mail-function/configuration problem; order creation still succeeded.
- **Why are follow-ups dated separately?** They were performed later. Evidence should not suggest they were captured during the original checkout.
- **How will the UI test repeat?** It creates a timestamp/UUID product, fresh guest session and fictional email, uses waits and verifies page values. Two real passing executions are still required.
