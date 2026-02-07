import '@/css/main.css';
import '@/js/main.js';
import '@/js/select2.min.js';
import htmx from 'htmx.org';
import $ from 'jquery';

console.log("yo yo");

// Make HTMX globally available
window.htmx = htmx;

// Make jquery globally available
window.$ = $;
window.jQuery = $; // Not sure about this one
if (window.jQuery) {
    console.log("jquery loaded.", jQuery.fn.jquery);
} else {
    console.error("jquery did not load.");
}

if (window.$) {
    console.log("jquery ok.", jQuery.fn.jquery);
} else {
    console.error("jquery not ok.");
}