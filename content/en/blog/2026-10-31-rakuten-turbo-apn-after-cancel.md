---
title: "Can a Rakuten Turbo Still Be Useful After Cancellation? POVO SIM Connects Successfully"
date: 2026-10-31T12:00:00+09:00
author: "Giko"
image: "/images/posts/rakuten-turbo-apn-illustration.png"
categories: ["Technology", "Networking"]
tags: ["Rakuten Turbo", "R2314M", "APN", "China Mobile", "povo 2.0"]
draft: false
---

I thought a Rakuten Turbo had little use after cancelling its service. A test with my own device today suggests it may have another life. I was thrilled when I saw it connect, and I wanted to share the result with more people in Japan, especially anyone unsure what to do with their device after cancelling.

## What worked in my test

On my Rakuten Turbo, I was able to set the APN through an API while running firmware 1.3.19. With a China Mobile SIM installed in Chiba, Japan, the device roamed onto the Japanese au network and showed a 4G/5G signal. A tablet connected to the router over Wi-Fi could access the internet.

Because my device is running firmware 1.3.19, I did not use any vulnerability in this test; I only changed the APN through the API. Firmware downgrading carries risks, so I did not try it. I also found that the Engineer interface appears to be inaccessible now.

Even so, being able to change the APN and connect to a network using a different SIM was enough to show that the device still has practical use. That was an encouraging result.

In my setup, this suggests the Rakuten Turbo I expected to leave unused after cancellation may work as a SIM router. It was a satisfying surprise to see a device headed for storage come back to life.

## The project I used

I referred to [Rakuten5GTurboAPI](https://github.com/0xNslabs/Rakuten5GTurboAPI), a proof-of-concept API project for the Rakuten 5G Turbo (R2314M). It includes functions that use known vulnerabilities and exposes an API for setting the APN. I used only the APN-setting function and did not use any vulnerability in this test. Its README lists CVE-2024-47865, CVE-2024-48895, and CVE-2024-52033.

This is not an official reuse method from Rakuten Mobile, and it does not mean every device, SIM, or region will work. My result applies only to the device, SIM, and network I tested. I did not use a vulnerability in this test, though the project does include vulnerability-related functions that can carry device and security risks. If you consider trying them, use only equipment you own or manage, and read the project details and risks first.

## povo 2.0 SIM also connected successfully

I later tested a povo 2.0 SIM in this Rakuten Turbo and confirmed that it connected to the internet. In my device and test setup, both the China Mobile SIM and the povo 2.0 SIM worked.

I also wanted to try Rakuten Saikyo Plan (Data Type), but Rakuten Mobile suspended new applications for that plan on March 5, 2026. New applications remain unavailable until Rakuten announces that they have resumed. [Rakuten Mobile's notice (Japanese)](https://network.mobile.rakuten.co.jp/information/news/service/3652/)

## For other Rakuten Turbo owners

These tests do not show that everyone can reuse a Rakuten Turbo after cancelling. In my setup, APN configuration worked on firmware 1.3.19, the China Mobile SIM connected through au roaming, and the povo 2.0 SIM also connected to the internet. These results show that a cancelled Rakuten Turbo can still be useful. I hope more people in Japan, especially those with an idle device after cancellation, will find this hands-on result.
