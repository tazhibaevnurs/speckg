(function () {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  // Mobile nav
  const toggle = $("[data-nav-toggle]");
  const mobile = $("[data-nav-mobile]");
  if (toggle && mobile) {
    toggle.addEventListener("click", () => {
      const open = !mobile.classList.contains("is-open");
      mobile.classList.toggle("is-open", open);
      if (open) mobile.removeAttribute("hidden");
      else mobile.setAttribute("hidden", "");
      toggle.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("nav-open", open);
    });
  }

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  document.body.classList.add("is-ready");
  window.addEventListener("pageshow", () => document.body.classList.remove("is-leaving"));

  const header = $(".site-header");
  const progress = $(".scroll-progress");
  const onScrollChrome = () => {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 10);
    if (progress) {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const p = max > 0 ? (window.scrollY / max) * 100 : 0;
      progress.style.width = `${p}%`;
    }
    const media = $(".hero-media");
    if (media && !reduced && window.scrollY < window.innerHeight) {
      media.style.transform = `translate3d(0, ${window.scrollY * 0.18}px, 0)`;
    }
  };
  onScrollChrome();
  window.addEventListener("scroll", onScrollChrome, { passive: true });

  if (!reduced) {
    $$(".js-split, .page-hero h1").forEach((el) => {
      const text = el.textContent.trim();
      el.setAttribute("aria-label", text);
      el.classList.add("is-split");
      let i = 0;
      el.innerHTML = text
        .split(/(\s+)/)
        .map((chunk) => {
          if (/^\s+$/.test(chunk)) return chunk;
          const html = `<span class="word"><span style="--i:${i}">${chunk}</span></span>`;
          i += 1;
          return html;
        })
        .join("");
    });

    const revealSel = [
      ".advantage",
      ".vehicle-card",
      ".steps li",
      ".lineup li",
      ".trust-list li",
      ".aside-card",
      ".doc-card",
      ".footer-grid > *",
    ].join(",");
    const items = $$(revealSel);
    items.forEach((el) => {
      const parent = el.parentElement;
      if (!parent) return;
      const pack = items.filter((node) => node.parentElement === parent);
      const idx = pack.indexOf(el);
      if (idx > 0) el.style.setProperty("--reveal-delay", `${Math.min(idx, 7) * 80}ms`);
    });
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px 12% 0px" }
    );
    items.forEach((el) => {
      io.observe(el);
      if (el.getBoundingClientRect().top < window.innerHeight * 0.96) {
        el.classList.add("is-in");
      }
    });
    setTimeout(() => items.forEach((el) => el.classList.add("is-in")), 1800);

    const seen = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("is-seen");
        });
      },
      { threshold: 0.12 }
    );
    $$(".section").forEach((el) => seen.observe(el));

    const hero = $(".hero");
    if (hero && finePointer) {
      hero.addEventListener("mousemove", (e) => {
        const r = hero.getBoundingClientRect();
        hero.style.setProperty("--mx", `${((e.clientX - r.left) / r.width) * 100}%`);
        hero.style.setProperty("--my", `${((e.clientY - r.top) / r.height) * 100}%`);
      });
    }

    if (finePointer) {
      $$(".vehicle-card").forEach((card) => {
        card.addEventListener("mousemove", (e) => {
          const r = card.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width - 0.5;
          const y = (e.clientY - r.top) / r.height - 0.5;
          card.style.transform = `perspective(900px) rotateY(${x * 7}deg) rotateX(${-y * 6}deg) translateY(-7px)`;
        });
        card.addEventListener("mouseleave", () => {
          card.style.transform = "";
        });
      });
      $$(".btn-gold").forEach((btn) => {
        btn.addEventListener("mousemove", (e) => {
          const r = btn.getBoundingClientRect();
          const x = (e.clientX - r.left - r.width / 2) * 0.12;
          const y = (e.clientY - r.top - r.height / 2) * 0.16;
          btn.style.transform = `translate(${x}px, ${y}px)`;
        });
        btn.addEventListener("mouseleave", () => {
          btn.style.transform = "";
        });
      });
    }

    document.addEventListener("click", (e) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = e.target.closest("a");
      if (!a || !a.href || a.target === "_blank" || a.hasAttribute("download")) return;
      const url = new URL(a.href, window.location.href);
      if (url.origin !== window.location.origin) return;
      if (url.pathname === window.location.pathname && url.search === window.location.search) return;
      if (a.getAttribute("href").startsWith("#")) return;
      e.preventDefault();
      document.body.classList.add("is-leaving");
      window.setTimeout(() => {
        window.location.href = a.href;
      }, 380);
    });
  }

  // Lead modal
  const modal = $("[data-lead-modal]");
  let modalTimer;
  function openLead(btn) {
    if (!modal) return;
    const title = $("#lead-modal-title");
    const form = $("form", modal);
    const type = btn.getAttribute("data-form-type") || "general";
    const source = btn.getAttribute("data-source") || "Модальное окно";
    if (title) {
      const labels = {
        callback: "Заказать звонок",
        vehicle: "Запросить машину",
        calculator: "Точный расчёт",
        general: "Оставить заявку",
      };
      title.textContent = labels[type] || labels.general;
    }
    if (form) {
      const typeInput = form.querySelector('[name="form_type"]');
      const sourceInput = form.querySelector('[name="source"]');
      if (typeInput) typeInput.value = type;
      if (sourceInput) sourceInput.value = source;
      const extra = form.querySelector("[data-extra-json]");
      if (extra && type === "calculator" && window.__lastCalc) {
        extra.value = JSON.stringify(window.__lastCalc);
      }
    }
    clearTimeout(modalTimer);
    modal.removeAttribute("hidden");
    requestAnimationFrame(() => modal.classList.add("is-open"));
    document.body.classList.add("nav-open");
  }
  function closeLead() {
    if (!modal) return;
    modal.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    const hide = () => modal.setAttribute("hidden", "");
    if (reduced) hide();
    else modalTimer = setTimeout(hide, 420);
  }
  $$("[data-open-lead]").forEach((btn) =>
    btn.addEventListener("click", () => openLead(btn))
  );
  $$("[data-close-lead]").forEach((el) => el.addEventListener("click", closeLead));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeLead();
  });

  // AJAX forms
  $$("[data-lead-form]").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector('[type="submit"]');
      const prev = btn ? btn.textContent : "";
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Отправляем…";
      }
      try {
        const res = await fetch(form.action, {
          method: "POST",
          body: new FormData(form),
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
        const data = await res.json().catch(() => ({}));
        if (res.ok && data.ok) {
          form.reset();
          alert(data.message || "Заявка принята.");
          closeLead();
        } else {
          alert("Проверьте имя и телефон.");
        }
      } catch (err) {
        alert("Сеть недоступна. Напишите в Telegram.");
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.textContent = prev;
        }
      }
    });
  });

  // Calculator
  function fmt(n) {
    return Math.round(n)
      .toString()
      .replace(/\B(?=(\d{3})+(?!\d))/g, " ") + " ₽";
  }
  $$("[data-calc-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const type = form.type.value;
      const rf = Number(String(form.rf_price.value).replace(/\s/g, "").replace(",", ".")) || 0;
      const usd = Number(String(form.our_price_usd.value).replace(/\s/g, "").replace(",", ".")) || 0;
      const rate = (window.SPEC && window.SPEC.usdRub) || 90;
      const utilMap = (window.SPEC && window.SPEC.utilFee) || {};
      const util = utilMap[type] || utilMap.other || 0;
      const ourRub = usd * rate;
      const delta = rf - ourRub;
      const box = form.closest("[data-calculator]")?.querySelector("[data-calc-result]");
      if (!box) return;
      box.hidden = false;
      const countTo = (el, value, prefix) => {
        if (!el) return;
        if (reduced) {
          el.textContent = prefix + fmt(value);
          return;
        }
        const start = performance.now();
        const tick = (now) => {
          const p = Math.min(1, (now - start) / 900);
          const eased = 1 - (1 - p) ** 3;
          el.textContent = prefix + fmt(value * eased);
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      };
      const deltaEl = box.querySelector("[data-calc-delta]");
      countTo(deltaEl, delta, delta >= 0 ? "≈ " : "разница ≈ ");
      countTo(box.querySelector("[data-calc-our-rub]"), ourRub, "");
      countTo(box.querySelector("[data-calc-rf]"), rf, "");
      countTo(box.querySelector("[data-calc-util]"), util, "");
      window.__lastCalc = {
        type,
        rf_price_rub: rf,
        our_price_usd: usd,
        our_price_rub: Math.round(ourRub),
        util_fee_rub: util,
        delta_rub: Math.round(delta),
        rate,
      };
    });
  });

  // Gallery
  $$("[data-gallery]").forEach((gallery) => {
    const main = gallery.querySelector("[data-gallery-main]");
    $$("[data-thumb]", gallery).forEach((btn) => {
      btn.addEventListener("click", () => {
        if (!main) return;
        const next = btn.getAttribute("data-thumb");
        if (!next || main.src.endsWith(next)) return;
        main.style.opacity = "0";
        window.setTimeout(() => {
          main.src = next;
          main.style.opacity = "1";
        }, 180);
      });
    });
  });

  // Smooth in-page buttons
  $$("[data-scroll]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const el = document.querySelector(btn.getAttribute("data-scroll"));
      if (el) el.scrollIntoView({ behavior: "smooth" });
    });
  });
})();
