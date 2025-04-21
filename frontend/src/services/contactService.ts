import api from "./api";
import { useUserStore } from "../store/userStore";

export interface ContactFormData {
  subject: string;
  message: string;
  alt_email?: string;
  phone?: string;
}

const getAuthHeaders = () => {
  const userStore = useUserStore();
  return {
    headers: {
      Authorization: `Bearer ${userStore.token}`,
    },
  };
};

export const sendContactMessage = async (
  data: ContactFormData
): Promise<void> => {
  try {
    const headers = getAuthHeaders();
    // console.log("🟡 Contact Payload:", data);
    // console.log("🟡 Contact Headers:", headers);

    await api.post("/api/accounts/contact/", data, headers);

    // console.log("🟢 Backend response:", response.status, response.data);
  } catch (error: any) {
    console.error(
      "❌ Error sending contact message:",
      error.response?.data || error.message
    );
    throw new Error(
      error.response?.data?.message || "Failed to send contact message"
    );
  }
};
