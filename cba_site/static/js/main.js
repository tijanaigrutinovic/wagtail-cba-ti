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

    function init() {
        initFaqSections();
        initHomeLearningTabs();
    }

    window.toggleFaq = toggleFaq;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
