async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Accept": "application/json" },
    credentials: "same-origin",
    ...options
  });
  const contentType = res.headers.get("content-type") || "";
  let data = null;
  if (contentType.includes("application/json")) {
    data = await res.json();
  } else {
    data = { ok: res.ok };
  }
  if (!res.ok) throw { status: res.status, data };
  return data;
}

function showAlert(message, type="success") {
  const area = document.getElementById("alertArea");
  if (!area) return;
  area.innerHTML = `<div class="alert alert-${type} alert-dismissible" role="alert">
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  </div>`;
}

async function refreshAuthUI() {
  try {
    const resp = await api("/whoami");
    const auth = resp.user;
    const authArea = document.getElementById("authArea");
    const createBtn = document.getElementById("createBtn");
    if (!authArea) return;
    if (auth) {
      authArea.innerHTML = `
        <span class="me-2">Hi, <strong>${auth.name}</strong></span>
        <a class="btn btn-outline-secondary" href="/events/new">Create</a>
        <form id="logoutForm" class="ms-2">
          <button class="btn btn-outline-danger" type="submit">Logout</button>
        </form>`;
      if (createBtn) createBtn.style.display = "";
      document.querySelectorAll(".owner-only").forEach(btn => {
        const ownerId = btn.getAttribute("data-owner");
        if (String(ownerId) !== String(auth.id)) btn.style.display = "none";
      });
      const lf = document.getElementById("logoutForm");
      if (lf) {
        lf.addEventListener("submit", async (e) => {
          e.preventDefault();
          try {
            await api("/auth/logout", { method: "POST" });
            window.location.href = "/";
          } catch (err) {
            showAlert("Logout failed", "danger");
          }
        });
      }
    } else {
      authArea.innerHTML = `
        <a class="btn btn-outline-primary" href="/login">Login</a>
        <a class="btn btn-primary ms-2" href="/register">Register</a>`;
      if (createBtn) createBtn.style.display = "none";
      document.querySelectorAll(".owner-only").forEach(btn => btn.style.display = "none");
    }
  } catch (e) {}
}

document.addEventListener("DOMContentLoaded", () => {
  refreshAuthUI();

  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(loginForm);
      try {
        await api("/auth/login", { method: "POST", body: form });
        window.location.href = "/";
      } catch (err) {
        const msg = err?.data?.errors?.general || "Login failed";
        showAlert(msg, "danger");
      }
    });
  }

  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(registerForm);
      try {
        await api("/auth/register", { method: "POST", body: form });
        window.location.href = "/";
      } catch (err) {
        const errors = err?.data?.errors || {};
        const first = Object.values(errors)[0] || "Registration failed";
        showAlert(first, "danger");
      }
    });
  }

  const eventForm = document.getElementById("eventForm");
  if (eventForm) {
    eventForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const form = new FormData(eventForm);
      try {
        await api("/events", { method: "POST", body: form });
        showAlert("Event created!");
        setTimeout(() => (window.location.href = "/"), 500);
      } catch (err) {
        const errors = err?.data?.errors || {};
        const first = Object.values(errors)[0] || "Create failed";
        showAlert(first, "danger");
      }
    });
  }

  const eventEditForm = document.getElementById("eventEditForm");
  if (eventEditForm) {
    eventEditForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = eventEditForm.getAttribute("data-id");
      const form = new FormData(eventEditForm);
      try {
        await api(`/events/${id}`, { method: "PUT", body: form });
        showAlert("Event updated!");
        setTimeout(() => (window.location.href = "/events/" + id), 500);
      } catch (err) {
        const errors = err?.data?.errors || {};
        const first = Object.values(errors)[0] || "Update failed";
        showAlert(first, "danger");
      }
    });
  }

  const deleteBtn = document.getElementById("deleteBtn");
  if (deleteBtn) {
    deleteBtn.addEventListener("click", async () => {
      const id = deleteBtn.getAttribute("data-id");
      if (!confirm("Delete this event?")) return;
      try {
        await api(`/events/${id}`, { method: "DELETE" });
        window.location.href = "/";
      } catch (err) {
        showAlert("Delete failed", "danger");
      }
    });
  }
});
