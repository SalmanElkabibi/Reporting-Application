/*
 FireShot - Webpage Screenshots and Annotations
 Copyright (C) 2007-2021 Evgeny Suslikov (evgeny@suslikov.ru)
*/
function addHandlers(){$("#btnAddPermissions").click(function(){addTabsPermission(function(){alert("Thank you, you can now use FireShot.");window.close()},function(){})});$("#btnAddGMailPermission").click(function(){addGmailPermission(function(){chrome.extension.getBackgroundPage().openGmailComposer();window.close()},function(){alert("Permission not granted, FireShot will not be able to create Gmail attachments.")})})}
document.addEventListener("DOMContentLoaded",function(){$(isWindows()?"#imgPermisionsDialogWindows":"#imgPermisionsDialogMac").show();addHandlers()});window.addEventListener("unload",function(){getExtension().fPermissionsPageOpened=!1});
