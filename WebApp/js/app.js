const DEFAULT_API_URL = "http://localhost:8000";
const STORAGE_KEY = "logitrack_auth";
const API_URL_KEY = "logitrack_api_url";

const PRICE_RULES = {
  office: { base: 5, perKg: 1.2 },
  address: { base: 8, perKg: 1.6 },
};

const elements = {
  apiBaseUrl: document.getElementById("apiBaseUrl"),
  saveApiBtn: document.getElementById("saveApiBtn"),
  registerForm: document.getElementById("registerForm"),
  loginForm: document.getElementById("loginForm"),
  logoutBtn: document.getElementById("logoutBtn"),
  authUser: document.getElementById("authUser"),
  messageArea: document.getElementById("messageArea"),
  shipmentsBody: document.getElementById("shipmentsBody"),
  refreshShipmentsBtn: document.getElementById("refreshShipmentsBtn"),
  shipmentScope: document.getElementById("shipmentScope"),
  createShipmentForm: document.getElementById("createShipmentForm"),
  updateShipmentForm: document.getElementById("updateShipmentForm"),
  deliveryType: document.getElementById("deliveryType"),
  weight: document.getElementById("weight"),
  pricePreview: document.getElementById("pricePreview"),
  refreshUsersBtn: document.getElementById("refreshUsersBtn"),
  usersBody: document.getElementById("usersBody"),
  createEmployeeForm: document.getElementById("createEmployeeForm"),
};

const state = {
  token: null,
  role: null,
  user: null,
  apiUrl: DEFAULT_API_URL,
};

const endpoints = {
  register: "/auth/register",
  login: "/auth/login",
  shipments: "/shipments",
  updateShipmentStatus: (id) => `/shipments/${id}/status`,
  users: "/users",
  createEmployee: "/users/employees",
  updateRole: (id) => `/users/${id}/role`,
};

function loadState() {
  const savedAuth = localStorage.getItem(STORAGE_KEY);
  if (savedAuth) {
    try {
      const parsed = JSON.parse(savedAuth);
      state.token = parsed.token;
      state.role = parsed.role;
      state.user = parsed.user;
    } catch (error) {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  const savedApiUrl = localStorage.getItem(API_URL_KEY);
  if (savedApiUrl) {
    state.apiUrl = savedApiUrl;
  }
  elements.apiBaseUrl.value = state.apiUrl;
}

function persistAuth() {
  if (state.token) {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ token: state.token, role: state.role, user: state.user })
    );
  } else {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function persistApiUrl() {
  localStorage.setItem(API_URL_KEY, state.apiUrl);
}

function showMessage(text, type = "info") {
  elements.messageArea.className = `message message--${type}`;
  elements.messageArea.textContent = text;
}

function setAuthState({ token, role, user }) {
  state.token = token;
  state.role = role;
  state.user = user;
  persistAuth();
  renderAuthState();
  renderRolePanels();
}

function renderAuthState() {
  if (state.token) {
    elements.authUser.textContent = `${state.user?.name || "User"} (${state.role})`;
    elements.logoutBtn.disabled = false;
  } else {
    elements.authUser.textContent = "Not signed in";
    elements.logoutBtn.disabled = true;
  }
}

function renderRolePanels() {
  document.querySelectorAll("[data-role]").forEach((section) => {
    const requiredRole = section.getAttribute("data-role");
    const visible = state.role === requiredRole || state.role === "administrator";
    section.style.display = visible ? "block" : "none";
  });
}

function getHeaders() {
  const headers = { "Content-Type": "application/json" };
  if (state.token) {
    headers.Authorization = `Bearer ${state.token}`;
  }
  return headers;
}

async function apiRequest(path, options = {}) {
  const response = await fetch(`${state.apiUrl}${path}`, {
    ...options,
    headers: { ...getHeaders(), ...(options.headers || {}) },
  });

  let data = null;
  const text = await response.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { detail: text };
    }
  }

  if (!response.ok) {
    const message =
      data?.detail || data?.message || "Request failed. Check API settings.";
    throw new Error(message);
  }

  return data;
}

function validateShipmentForm(formData) {
  const weight = Number(formData.weight);
  if (!formData.sender || !formData.receiver || !formData.destination) {
    throw new Error("Sender, receiver, and destination are required.");
  }
  if (Number.isNaN(weight) || weight <= 0) {
    throw new Error("Weight must be a positive number.");
  }
}

function calculatePrice(weight, deliveryType) {
  const rule = PRICE_RULES[deliveryType] || PRICE_RULES.office;
  return rule.base + rule.perKg * weight;
}

function renderPricePreview() {
  const weight = Number(elements.weight.value);
  if (Number.isNaN(weight) || weight <= 0) {
    elements.pricePreview.textContent = "$0.00";
    return;
  }
  const price = calculatePrice(weight, elements.deliveryType.value);
  elements.pricePreview.textContent = `$${price.toFixed(2)}`;
}

function renderShipments(shipments = []) {
  if (!shipments.length) {
    elements.shipmentsBody.innerHTML =
      '<tr><td colspan="7" class="empty">No shipments found.</td></tr>';
    return;
  }

  elements.shipmentsBody.innerHTML = shipments
    .map((shipment) => {
      return `
        <tr>
          <td>${shipment.id ?? "-"}</td>
          <td>${shipment.sender}</td>
          <td>${shipment.receiver}</td>
          <td>${shipment.deliveryType} - ${shipment.destination}</td>
          <td>${shipment.weight}</td>
          <td>$${Number(shipment.price).toFixed(2)}</td>
          <td>${shipment.status}</td>
        </tr>
      `;
    })
    .join("");
}

function renderUsers(users = []) {
  if (!users.length) {
    elements.usersBody.innerHTML =
      '<tr><td colspan="4" class="empty">No users found.</td></tr>';
    return;
  }

  elements.usersBody.innerHTML = users
    .map(
      (user) => `
        <tr>
          <td>${user.name || "-"}</td>
          <td>${user.email}</td>
          <td>
            <select data-role-select data-user-id="${user.id}">
              <option value="client" ${user.role === "client" ? "selected" : ""}>
                Client
              </option>
              <option value="employee" ${
                user.role === "employee" ? "selected" : ""
              }>
                Employee
              </option>
              <option value="administrator" ${
                user.role === "administrator" ? "selected" : ""
              }>
                Administrator
              </option>
            </select>
          </td>
          <td>
            <button class="btn btn--ghost" data-role-save data-user-id="${user.id}">
              Save
            </button>
          </td>
        </tr>
      `
    )
    .join("");
}

async function refreshShipments() {
  if (!state.token) {
    elements.shipmentScope.textContent = "Sign in to view shipments.";
    renderShipments([]);
    return;
  }

  const data = await apiRequest(endpoints.shipments);
  renderShipments(data?.items || data || []);

  if (state.role === "client") {
    elements.shipmentScope.textContent = "Showing your shipments only.";
  } else {
    elements.shipmentScope.textContent = "Showing all shipments.";
  }
}

async function refreshUsers() {
  if (state.role !== "administrator") {
    renderUsers([]);
    return;
  }
  const data = await apiRequest(endpoints.users);
  renderUsers(data?.items || data || []);
}

elements.saveApiBtn.addEventListener("click", () => {
  const value = elements.apiBaseUrl.value.trim();
  if (!value) {
    showMessage("Please enter a valid API base URL.", "error");
    return;
  }
  state.apiUrl = value.replace(/\/$/, "");
  persistApiUrl();
  showMessage("API base URL saved.", "success");
});

elements.registerForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.target));
  try {
    await apiRequest(endpoints.register, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    showMessage("Registration successful. You can log in now.", "success");
    event.target.reset();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.target));
  try {
    const data = await apiRequest(endpoints.login, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setAuthState({
      token: data.access_token || data.token,
      role: data.role,
      user: data.user,
    });
    showMessage("Logged in successfully.", "success");
    await refreshShipments();
    await refreshUsers();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.logoutBtn.addEventListener("click", () => {
  setAuthState({ token: null, role: null, user: null });
  renderShipments([]);
  renderUsers([]);
  showMessage("Logged out.", "info");
});

elements.refreshShipmentsBtn.addEventListener("click", async () => {
  try {
    await refreshShipments();
    showMessage("Shipments refreshed.", "success");
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.deliveryType.addEventListener("change", renderPricePreview);
elements.weight.addEventListener("input", renderPricePreview);

elements.createShipmentForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.target));
  try {
    validateShipmentForm(payload);
    const price = calculatePrice(Number(payload.weight), payload.deliveryType);
    const shipmentPayload = {
      ...payload,
      weight: Number(payload.weight),
      price,
    };
    await apiRequest(endpoints.shipments, {
      method: "POST",
      body: JSON.stringify(shipmentPayload),
    });
    showMessage("Shipment created.", "success");
    event.target.reset();
    renderPricePreview();
    await refreshShipments();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.updateShipmentForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.target));
  try {
    await apiRequest(endpoints.updateShipmentStatus(payload.shipmentId), {
      method: "PATCH",
      body: JSON.stringify({ status: payload.status }),
    });
    showMessage("Shipment status updated.", "success");
    event.target.reset();
    await refreshShipments();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.refreshUsersBtn.addEventListener("click", async () => {
  try {
    await refreshUsers();
    showMessage("Users refreshed.", "success");
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.createEmployeeForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.target));
  try {
    await apiRequest(endpoints.createEmployee, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    showMessage("Employee created.", "success");
    event.target.reset();
    await refreshUsers();
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.usersBody.addEventListener("click", async (event) => {
  const target = event.target;
  if (!target.matches("[data-role-save]")) return;

  const userId = target.getAttribute("data-user-id");
  const select = elements.usersBody.querySelector(
    `[data-role-select][data-user-id="${userId}"]`
  );
  if (!select) return;

  try {
    await apiRequest(endpoints.updateRole(userId), {
      method: "PATCH",
      body: JSON.stringify({ role: select.value }),
    });
    showMessage("User role updated.", "success");
  } catch (error) {
    showMessage(error.message, "error");
  }
});

loadState();
renderAuthState();
renderRolePanels();
renderPricePreview();
if (state.token) {
  refreshShipments();
  refreshUsers();
}
