// content.js
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if( request.message === "clicked_browser_action" ) {
      //var firstHref = $("a[href^='http']").eq(0).attr("href");
	  var firstHref = $(location).attr("href");

	  var pw_url = "http://www.pwbreaker.com/index?url=" + encodeURIComponent(firstHref);

      //console.log("http://www.pwbreaker.com");

      // This line is new!
      chrome.runtime.sendMessage({"message": "open_new_tab", "url": pw_url});
    }
  }
);