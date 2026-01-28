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
  viewSentBtn: document.getElementById("viewSentBtn"),
  viewReceivedBtn: document.getElementById("viewReceivedBtn"),
  senderSelect: document.getElementById("sender"),
  receiverSelect: document.getElementById("receiver"),
  officeSelect: document.getElementById("destinationOffice"),
  officeWrapper: document.getElementById("officeSelectWrapper"),
  addressWrapper: document.getElementById("addressInputWrapper"),
  companySelect: document.getElementById("shipmentCompany"),
  adminCompanyWrapper: document.getElementById("adminCompanySelect"),
};

const state = {
  token: null,
  role: null,
  user: null,
  apiUrl: DEFAULT_API_URL,
};

const endpoints = {
  // Authentication & Registration
  register: "/api/v1/register/organization",
  login: "/api/v1/auth/token",

  // Shipments
  shipments: "/api/v1/shipments",
  createShipment: "/api/v1/shipments",
  updateShipmentStatus: (id) => `/api/v1/shipments/${id}/status`,

  // Users
  users: "/api/v1/users",
  createEmployee: "/api/v1/users",
  updateRole: (id) => `/api/v1/users/${id}`,

  // Client Specific Views
  clientSent: (id) => `/api/v1/shipments/client/${id}/sent`,
  clientReceived: (id) => `/api/v1/shipments/client/${id}/received`,

  // Entities for Selects
  clients: "/api/v1/users/clients",
  offices: "/api/v1/offices",
  companies: "/api/v1/companies",
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
    const visible = state.role === requiredRole || state.role === "admin" || state.role === "super_admin";
    section.style.display = visible ? (section.tagName === "BUTTON" ? "inline-block" : "block") : "none";
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
    let message = data?.detail || data?.message || "Request failed. Check API settings.";
    if (typeof message === "object") {
      message = JSON.stringify(message, null, 2);
    }
    throw new Error(message);
  }

  return data;
}

function validateShipmentForm(formData) {
  const weight = Number(formData.weight);
  if (!formData.sender_id || !formData.receiver_id) {
    throw new Error("Sender and receiver are required.");
  }
  if (formData.is_to_office === "true" && !formData.destination_office_id) {
    throw new Error("Please select a destination office.");
  }
  if (formData.is_to_office === "false" && !formData.delivery_address) {
    throw new Error("Please enter a delivery address.");
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
  const typeKey = elements.deliveryType.value === "true" ? "office" : "address";
  let price = calculatePrice(weight, typeKey);
  if (elements.deliveryType.value === "true") {
    price = price * 0.8; // Apply the 20% backend discount preview
  }
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
              <option value="employee" ${user.role === "employee" ? "selected" : ""
        }>
                Employee
              </option>
              <option value="admin" ${user.role === "admin" ? "selected" : ""
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

async function refreshShipments(specificPath = null, scopeText = null) {
  if (!state.token) {
    elements.shipmentScope.textContent = "Sign in to view shipments.";
    renderShipments([]);
    return;
  }

  const path = specificPath || endpoints.shipments;
  const data = await apiRequest(path);
  renderShipments(data?.items || data || []);

  if (scopeText) {
    elements.shipmentScope.textContent = scopeText;
  } else if (state.role === "client") {
    elements.shipmentScope.textContent = "Showing your shipments only.";
  } else {
    elements.shipmentScope.textContent = "Showing all shipments.";
  }
}

async function refreshUsers() {
  if (state.role !== "admin" && state.role !== "super_admin") {
    renderUsers([]);
    return;
  }
  const data = await apiRequest(endpoints.users);
  renderUsers(data?.items || data || []);

  // Also refresh the dropdowns to reflect new clients
  await populateSelects();
}

async function populateSelects() {
  if (!state.token) return;

  // Helper to populate a specific select
  async function fill(endpoint, element, label, mapper) {
    try {
      console.log(`Fetching ${label} from ${endpoint}...`);
      const data = await apiRequest(endpoint);
      const items = data?.items || data || [];
      console.log(`Fetched ${items.length} ${label}(s).`);

      if (items.length === 0) {
        element.innerHTML = `<option value="">-- No ${label} found --</option>`;
      } else {
        const options = items.map(mapper).join("");
        element.innerHTML = `<option value="">-- Select ${label} --</option>${options}`;
      }
    } catch (error) {
      console.error(`Failed to fetch ${label}:`, error);
      element.innerHTML = `<option value="">-- Error loading ${label} (${error.message}) --</option>`;
    }
  }

  // Fetch independently
  fill(endpoints.clients, elements.senderSelect, "Sender", c =>
    `<option value="${c.id}">${c.first_name || ""} ${c.last_name || ""} (${c.email})</option>`);

  fill(endpoints.clients, elements.receiverSelect, "Receiver", c =>
    `<option value="${c.id}">${c.first_name || ""} ${c.last_name || ""} (${c.email})</option>`);

  fill(endpoints.offices, elements.officeSelect, "Office", o =>
    `<option value="${o.id}">${o.name} (${o.city})</option>`);

  // Admin company list - Only for Super Admin
  if (state.role === "super_admin") {
    elements.adminCompanyWrapper.style.display = "block";
    fill(endpoints.companies, elements.companySelect, "Company", c =>
      `<option value="${c.id}">${c.name}</option>`);
  } else {
    elements.adminCompanyWrapper.style.display = "none";
  }
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

  // FastAPI OAuth2PasswordRequestForm expects x-www-form-urlencoded
  // and field names 'username' and 'password'
  const formData = new URLSearchParams();
  formData.append("username", payload.email);
  formData.append("password", payload.password);

  try {
    const data = await apiRequest(endpoints.login, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });
    setAuthState({
      token: data.access_token || data.token,
      role: data.role,
      user: data.user,
    });
    showMessage("Logged in successfully.", "success");
    await refreshShipments();
    await refreshUsers();
    await populateSelects();
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
    showMessage("All relevant shipments refreshed.", "success");
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.viewSentBtn.addEventListener("click", async () => {
  try {
    const userId = state.user?.id;
    if (!userId) throw new Error("User ID not found.");
    await refreshShipments(endpoints.clientSent(userId), "Showing shipments sent by you.");
    showMessage("Sent shipments loaded.", "success");
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.viewReceivedBtn.addEventListener("click", async () => {
  try {
    const userId = state.user?.id;
    if (!userId) throw new Error("User ID not found.");
    await refreshShipments(endpoints.clientReceived(userId), "Showing shipments received by you.");
    showMessage("Received shipments loaded.", "success");
  } catch (error) {
    showMessage(error.message, "error");
  }
});

elements.deliveryType.addEventListener("change", () => {
  const isToOffice = elements.deliveryType.value === "true";
  elements.officeWrapper.style.display = isToOffice ? "block" : "none";
  elements.addressWrapper.style.display = isToOffice ? "none" : "block";
  renderPricePreview();
});
elements.weight.addEventListener("input", renderPricePreview);

elements.createShipmentForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData);

  try {
    validateShipmentForm(payload);

    const weight = Number(payload.weight);
    const typeKey = payload.is_to_office === "true" ? "office" : "address";
    const basePrice = calculatePrice(weight, typeKey);

    const shipmentPayload = {
      sender_id: payload.sender_id,
      receiver_id: payload.receiver_id,
      company_id: payload.company_id || state.user?.company_id,
      weight: weight,
      price: basePrice, // Backend will re-calculate but we send for logging
      is_to_office: payload.is_to_office === "true",
      origin_office_id: null,
      destination_office_id: payload.is_to_office === "true" ? payload.destination_office_id : null,
      delivery_address: payload.is_to_office === "false" ? payload.delivery_address : null,
    };

    if (!shipmentPayload.company_id) {
      throw new Error("Company ID is missing. Admin must select a company.");
    }

    await apiRequest(endpoints.shipments, {
      method: "POST",
      body: JSON.stringify(shipmentPayload),
    });
    showMessage("Shipment created successfully.", "success");
    event.target.reset();
    elements.officeWrapper.style.display = "block";
    elements.addressWrapper.style.display = "none";
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
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData);

  // Backend expects 'role' to be 'employee'
  // and does not yet support 'courier' or 'office_staff' enums.
  // We send the standardized role but keep the form data flexible.
  const finalPayload = {
    ...payload,
    role: "employee", // Standard role for compatibility
    first_name: payload.name.split(" ")[0] || "Employee",
    last_name: payload.name.split(" ").slice(1).join(" ") || "Staff",
  };

  try {
    await apiRequest(endpoints.createEmployee, {
      method: "POST",
      body: JSON.stringify(finalPayload),
    });
    showMessage(`Employee created as ${payload.employee_role.replace("_", " ")}.`, "success");
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
    await refreshUsers(); // Refresh table and dropdowns
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
  populateSelects();
}
