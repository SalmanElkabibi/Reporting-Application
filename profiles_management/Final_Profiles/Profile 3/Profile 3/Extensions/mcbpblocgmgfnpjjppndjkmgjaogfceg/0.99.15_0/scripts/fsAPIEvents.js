/*
 FireShot - Webpage Screenshots and Annotations
 Copyright (C) 2007-2021 Evgeny Suslikov (evgeny@suslikov.ru)
*/
window.fsAPIEvents||(window.fsAPIEvents=!0,chrome.runtime.sendMessage({message:"checkFSAvailabilityEvt"},function(a){document.addEventListener("checkFSAvailabilityEvt",function(c){for(var b in a)a.hasOwnProperty(b)&&c.target.setAttribute(b,a[b])},!1)}),document.addEventListener("capturePageEvt",function(a){chrome.runtime.sendMessage({message:"capturePageEvt",Entire:a.target.getAttribute("Entire"),Action:a.target.getAttribute("Action"),Data:a.target.getAttribute("Data"),CapturedElement:a.target.getAttribute("capturedFrameId")||
void 0},function(c){window.fsPendingCB=a.target.getAttribute("CBID")})},!1),document.addEventListener("switchToNativeEvt",function(){chrome.runtime.sendMessage({message:"switchToNativeEvt"},function(a){})},!1));
