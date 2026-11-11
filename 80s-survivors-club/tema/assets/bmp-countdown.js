/**
 * Countdown timer custom element for the announcement block.
 *
 * Feature-scoped module: loaded only from
 * snippets/bmp-countdown.liquid, at the render site of an active countdown.
 * The server (snippets/bmp-countdown.liquid) already rendered the correct
 * digits from `data-bmp-end`, so this element's only job is to keep them
 * ticking every second. Behavior mirrors the Symmetry theme's
 * countdown-timer.js reference (interval-driven, clearInterval at zero) —
 * rewritten for this element's own tag name and attribute contract, with no
 * digit-transition animations (YAGNI for v1).
 */
if (!customElements.get('bmp-countdown-timer')) {
  class BmpCountdownTimer extends HTMLElement {
    connectedCallback() {
      this.endTime = new Date(this.dataset.bmpEnd).getTime();
      if (Number.isNaN(this.endTime)) return;

      this.daysEl = this.querySelector('[data-bmp-countdown="days"]');
      this.hoursEl = this.querySelector('[data-bmp-countdown="hours"]');
      this.minutesEl = this.querySelector('[data-bmp-countdown="minutes"]');
      this.secondsEl = this.querySelector('[data-bmp-countdown="seconds"]');

      this.tick();
      this.interval = setInterval(this.tick.bind(this), 1000);
    }

    disconnectedCallback() {
      clearInterval(this.interval);
    }

    tick() {
      const remaining = this.endTime - Date.now();

      if (remaining <= 0) {
        clearInterval(this.interval);
        this.render(0, 0, 0, 0);
        return;
      }

      const totalSeconds = Math.floor(remaining / 1000);
      const days = Math.floor(totalSeconds / 86400);
      const hours = Math.floor((totalSeconds % 86400) / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;

      this.render(days, hours, minutes, seconds);
    }

    render(days, hours, minutes, seconds) {
      if (this.daysEl) this.daysEl.textContent = String(days);
      if (this.hoursEl) this.hoursEl.textContent = String(hours).padStart(2, '0');
      if (this.minutesEl) this.minutesEl.textContent = String(minutes).padStart(2, '0');
      if (this.secondsEl) this.secondsEl.textContent = String(seconds).padStart(2, '0');
    }
  }

  customElements.define('bmp-countdown-timer', BmpCountdownTimer);
}
