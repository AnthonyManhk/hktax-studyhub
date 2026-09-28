/* "AI Prompts" header button.
 *
 * Copies a hardened HK-tax prompt template to the clipboard so it can be
 * pasted into whatever AI the user already has open in their browser (Edge
 * Copilot, Chrome Gemini, or any chat AI) to set the background/instructions
 * before asking about a specific transaction.
 *
 * There is no API for a webpage to push a prompt directly into another
 * browser feature's own chat box, so this is a copy-to-clipboard helper,
 * not a live integration - the user still pastes it themselves.
 *
 * The prompt asks the AI to flag uncertainty rather than invent a plausible-
 * looking section or DIPN number, and states which year of assessment basis
 * to use by default, since neither is safe to leave to a general-purpose
 * model's own guess on a site built around the 2026/27-vs-2025/26 dual-year
 * distinction. Its citations are NOT checked by this Hub - unlike the
 * Transaction Checker's answers - and the modal says so every time.
 */
(function () {
  var PROMPT = [
    "You are a Hong Kong tax specialist. Work only from the Inland Revenue",
    "Ordinance (Cap. 112), the Stamp Duty Ordinance (Cap. 117), and current",
    "IRD DIPN/SOIPN guidance. If you are not certain a section or DIPN number",
    "is correct, say so explicitly rather than stating it with confidence.",
    "Use year of assessment 2026/27 (current law) unless told otherwise —",
    "if the question is about the ACCA TX-HKG exam basis instead, use 2025/26.",
    "",
    "Transaction: [describe the transaction here]",
    "",
    "Reference material from this page (optional — paste relevant text): [paste here]",
    "",
    "Provide:",
    "1. Taxability (which head of charge, if any)",
    "2. Deductibility (if an expense)",
    "3. The specific IRO/SDO section relied on",
    "4. Supporting DIPN/SOIPN, if any — say \"none found\" rather than guessing",
    "5. Risks and what to verify before relying on this for a filing position"
  ].join("\n");

  function fallbackCopy(text) {
    try {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.top = "-1000px";
      ta.style.left = "-1000px";
      document.body.appendChild(ta);
      ta.select();
      var ok = document.execCommand ? document.execCommand("copy") : false;
      document.body.removeChild(ta);
      return ok;
    } catch (e) {
      return false;
    }
  }

  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(
        function () { return true; },
        function () { return fallbackCopy(text); }
      );
    }
    return Promise.resolve(fallbackCopy(text));
  }

  function showModal(copied) {
    var existing = document.querySelector(".ai-prompt-modal");
    if (existing) existing.parentNode.removeChild(existing);

    var wrap = document.createElement("div");
    wrap.className = "ai-prompt-modal";
    wrap.innerHTML =
      '<div class="ai-prompt-box" role="dialog" aria-label="AI prompt">' +
        '<div class="ai-prompt-head">' +
          "<strong>AI Prompt" + (copied ? " — copied to clipboard" : "") + "</strong>" +
          '<button type="button" class="ai-prompt-close" aria-label="Close">&times;</button>' +
        "</div>" +
        '<p class="ai-prompt-note">' +
        (copied
          ? "Paste this into your browser's AI assistant (Edge Copilot, Chrome Gemini) or any chat AI, then fill in the transaction and paste any page text you want it to consider."
          : "Could not copy automatically — select the text below and press Ctrl+C (or Cmd+C), then paste it into your browser's AI assistant.") +
        "</p>" +
        '<textarea class="ai-prompt-text" readonly></textarea>' +
        '<p class="ai-prompt-warn">This calls a third-party AI outside this Hub. Its section and DIPN citations are not checked by this site — verify them the same way you would verify anything else here.</p>' +
      "</div>";
    document.body.appendChild(wrap);

    var textarea = wrap.querySelector(".ai-prompt-text");
    textarea.value = PROMPT;
    textarea.focus();
    textarea.select();

    function close() {
      if (wrap.parentNode) wrap.parentNode.removeChild(wrap);
      document.removeEventListener("keydown", onKey);
    }
    function onKey(ev) {
      if (ev.key === "Escape") close();
    }
    wrap.querySelector(".ai-prompt-close").addEventListener("click", close);
    wrap.addEventListener("click", function (ev) {
      if (ev.target === wrap) close();
    });
    document.addEventListener("keydown", onKey);
  }

  function wire() {
    var buttons = document.querySelectorAll(".ai-prompt-btn");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", function () {
        copy(PROMPT).then(showModal);
      });
    }
  }

  document.addEventListener("DOMContentLoaded", wire);
})();
