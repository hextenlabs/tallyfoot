---
layout: guide
title: Why do Apple Watch and iPhone show different step counts?
description: Apple Watch and iPhone count steps separately. Apple Health merges the two instead of adding them, using a priority list you can check and reorder.
lede: Apple Watch and iPhone each count steps with their own sensors, so their numbers differ. Apple Health does not add the two together but merges them into one total, and where both devices recorded the same steps, the source ranked higher in the Data Sources and Access list for Steps takes priority.
ct: guide-watch-vs-iphone
date: 2026-11-25
sources:
  - https://support.apple.com/en-us/108779
  - https://support.apple.com/en-us/105002
  - https://support.apple.com/guide/watch/track-daily-activity-apd3bf6d85a6/watchos
  - https://support.apple.com/guide/iphone/see-your-activity-summary-iph4c34a8a95/ios
  - https://developer.apple.com/forums/thread/710937
  - https://developer.apple.com/forums/thread/772068
  - https://developer.apple.com/forums/thread/804047
  - https://developer.apple.com/tutorials/data/documentation/healthkit/hkquantitytypeidentifier/stepcount.json
---
## The short answer

Your Apple Watch and your iPhone both count steps, each on its own. Apple's developer documentation for step data says the system records step samples automatically on iPhone and on Apple Watch. That leaves Apple Health with two overlapping records of the same day.

Health does not add them together, and it does not keep one device's day and discard the other's. It merges them. An Apple engineer [explained on the Apple Developer Forums](https://developer.apple.com/forums/thread/710937) that when someone has both an iPhone and an Apple Watch, data is collected on both, and the Health app relies on HealthKit's built-in source merging to turn the two streams into one estimate. Another Apple engineer [described the same process](https://developer.apple.com/forums/thread/772068) as de-duplicating data from different sources.

Where both devices recorded the same steps, a priority list decides which one counts. [Apple's support page on Health data](https://support.apple.com/en-us/108779) says that if multiple sources contribute the same data type, the source at the top of the list takes priority over the others. Steps that only one source recorded have nothing to compete with. The second engineer notes that the merged result can include data from other sources that does not overlap.

So the number in Health need not match either device's own count. It is one merged total. The pages cited here do not spell out the exact rules, and the first engineer says an app that tries to choose between overlapping samples by itself is unlikely to match HealthKit's merge.

## Which source Health ranks first

Apple says Health prioritizes data in this order by default:

1. Health data that you enter manually.
2. Data from your iPhone, iPad, and Apple Watch.
3. Data from apps and Bluetooth devices.

Apple Watch and iPhone sit in the same tier, and the support page does not say which of the two comes first. The list on your own iPhone settles it. To see the order, and change it if you want to:

1. Open the Health app on your iPhone.
2. Tap the Browse tab.
3. Tap Activity, then tap Steps.
4. Scroll down, then tap Data Sources & Access.
5. Tap Edit.
6. Touch and hold the Change Order button next to a source, then drag it up or down in the list.
7. Tap Done.

Only sources that contribute step data appear in this list. The support page does not recommend an order for the watch and the phone. A reasonable choice is to put the device that is on you for most of the day at the top.

## Why the two devices disagree

They sense different movement. Apple's iPhone guide says that [when you carry your iPhone with you](https://support.apple.com/guide/iphone/see-your-activity-summary-iph4c34a8a95/ios), its motion sensors track your steps, distance, and flights climbed. For the watch, Apple says the Activity app [relies on arm motion and an accelerometer](https://support.apple.com/en-us/105002) to track movement. A phone left on a desk while you walk to the kitchen is not being carried, so it has no record of that walk. A watch on your wrist can still count it.

They also do not share data instantly. The same Apple engineer who described de-duplication says the Health data stores on the watch and on the iPhone do not synchronize in real time, so a result can differ between the two until the watch's data has finished syncing to the iPhone. The engineer adds that the watch typically stores only about a week of Health data, while the iPhone has no such limit.

## Where each number shows up

- On Apple Watch, open the Activity app and turn the Digital Crown. Apple's watch guide lists total steps among the totals shown there.
- On iPhone, open the Fitness app, tap Summary, then tap the Step Count area.
- In the Health app, tap Browse, then Activity, then Steps. This is the merged total.

These screens do not all draw on the same sources. A developer whose app wrote steps to Health found them in the Health app but not in Fitness, and an Apple engineer [answered](https://developer.apple.com/forums/thread/804047) that this is expected: Health shows data from all sources, and Fitness does not show steps written by other apps. If an app or another tracker also writes steps on your phone, Health can count steps that Fitness does not.

## If the Health total looks wrong

Check three things.

First, look for a new source at the top of the list. Apple says new apps or devices that you add are listed at the top automatically, above your iPhone. If you recently connected a tracker or an app that writes steps, it may now outrank your own devices. In Data Sources & Access, tap Edit, then drag it lower, or tap the checkmark next to a third-party source to turn it off.

Second, look for manual entries, which rank above everything else by default. To remove one:

1. In the Health app, tap Browse, tap Activity, then tap Steps.
2. Scroll down to Options, then tap Show All Data.
3. Tap Edit.
4. Tap the Delete button next to the record you want to remove.
5. Tap Done.

Third, if the watch seems to contribute nothing, confirm that Fitness Tracking is on for it:

1. Open the Health app on your iPhone.
2. Tap the Profile button, then tap Devices.
3. Tap your Apple Watch.
4. Tap Privacy Settings and turn on Fitness Tracking.

## What a step app shows

A step app can show a third number, and the reason is the same merge. According to the engineer in [the first forum thread](https://developer.apple.com/forums/thread/710937), an app that asks HealthKit for statistics gets the same merging Health uses. An app that reads the raw samples has to pick between overlapping ones itself and is unlikely to match. That is one reason a third-party count can differ from the Steps total in Health.

If what you want is a step count on your watch face, see [How to put a step counter on your Apple Watch face]({{ "/apple-watch-step-counter" | relative_url }}). [Tallyfoot](STORE_URL) is one free option. Its App Store listing says it reads steps from Apple Health and your devices' motion sensors, and that it syncs between your own iPhone and Apple Watch.
