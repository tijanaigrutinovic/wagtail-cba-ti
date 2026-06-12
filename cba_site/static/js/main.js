/**
 * CBA Education — shared front-end behaviors (FAQ accordion, homepage tabs).
 */
(function () {
    'use strict';

    function toggleFaq(question) {
        var answer = question.nextElementSibling;
        if (!answer || !answer.classList.contains('faq-answer')) {
            answer = question.parentElement
                ? question.parentElement.querySelector(':scope > .faq-answer')
                : null;
        }
        if (!answer) return;

        var root = question.closest('.faq-section');
        var wasActive = question.classList.contains('active');

        if (root) {
            root.querySelectorAll('.faq-question').forEach(function (q) {
                q.classList.remove('active');
                q.setAttribute('aria-expanded', 'false');
            });
            root.querySelectorAll('.faq-answer').forEach(function (a) {
                a.classList.remove('active');
                a.style.removeProperty('display');
            });
        }

        if (!wasActive) {
            question.classList.add('active');
            question.setAttribute('aria-expanded', 'true');
            answer.classList.add('active');
            answer.style.setProperty('display', 'block', 'important');
        }
    }

    function initHomeLearningTabs() {
        document.querySelectorAll('.cba-home__learning').forEach(function (section) {
            var radios = section.querySelectorAll('.cba-home__tab-hack');
            var panels = section.querySelectorAll('.cba-home__tab-panel');
            var labels = section.querySelectorAll('.cba-home__tab-pill');

            if (!radios.length || !panels.length) return;

            function activateTab(index) {
                panels.forEach(function (panel, i) {
                    panel.style.display = i === index ? 'grid' : 'none';
                });
                labels.forEach(function (label, i) {
                    label.classList.toggle('is-active', i === index);
                });
                radios.forEach(function (radio, i) {
                    radio.setAttribute('aria-selected', i === index ? 'true' : 'false');
                });
            }

            radios.forEach(function (radio, index) {
                radio.addEventListener('change', function () {
                    if (radio.checked) activateTab(index);
                });
            });

            var initialIndex = 0;
            radios.forEach(function (radio, index) {
                if (radio.checked) initialIndex = index;
            });
            activateTab(initialIndex);
        });
    }

    function initFaqSections() {
        document.querySelectorAll('.faq-section').forEach(function (root) {
            root.addEventListener('click', function (e) {
                var question = e.target.closest('.faq-question');
                if (!question || !root.contains(question)) return;
                e.preventDefault();
                toggleFaq(question);
            });
        });
    }

    function initCookieBanner() {
        var banner = document.getElementById('cookie-banner');
        if (!banner) return;

        var CONSENT_KEY = 'cookie_consent';

        function hideBanner() {
            banner.classList.remove('is-visible');
            banner.classList.add('is-hidden');
            banner.setAttribute('aria-hidden', 'true');
        }

        function showBanner() {
            banner.classList.remove('is-hidden');
            banner.classList.add('is-visible');
            banner.setAttribute('aria-hidden', 'false');
        }

        function setConsent(value) {
            try {
                localStorage.setItem(CONSENT_KEY, value);
            } catch (e) {}
            window.cookieConsent = value;
            hideBanner();
            if (value === 'accepted') {
                loadAnalytics();
            }
        }

        function loadAnalytics() {
            // Load Google Analytics / other tracking here once tools are confirmed.
            // Example:
            // if (typeof gtag === 'function') { gtag('consent', 'update', { analytics_storage: 'granted' }); }
        }

        window.loadAnalytics = loadAnalytics;

        var acceptBtn = banner.querySelector('.cba-cookie-banner__accept');
        var declineBtn = banner.querySelector('.cba-cookie-banner__decline');

        if (acceptBtn) {
            acceptBtn.addEventListener('click', function () {
                setConsent('accepted');
            });
        }

        if (declineBtn) {
            declineBtn.addEventListener('click', function () {
                setConsent('declined');
            });
        }

        var existing = null;
        try {
            existing = localStorage.getItem(CONSENT_KEY);
        } catch (e) {}

        if (existing === 'accepted' || existing === 'declined') {
            window.cookieConsent = existing;
            hideBanner();
            if (existing === 'accepted') {
                loadAnalytics();
            }
            return;
        }

        showBanner();
    }

    function init() {
        initFaqSections();
        initHomeLearningTabs();
        initCookieBanner();
    }

    window.toggleFaq = toggleFaq;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
