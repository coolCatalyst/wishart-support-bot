import { supabaseUrl, supabaseKey, leadURL } from "../../config";
import axios from "axios";
import { createClient } from "@supabase/supabase-js";
import { config } from "../../config/config";

const baseURL = process.env.NEXT_PUBLIC_BACKEND_URL
const supabase = createClient(supabaseUrl, supabaseKey);
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
export async function getData(ID) {
  return config;
}

export async function postMessage(message, chat_history, setAnswer) {
  console.log("chathistory", chat_history);

  try {
    const response = await fetch(baseURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
        // Add other headers as needed
      },
      responseType: "stream",
      body: JSON.stringify({
        chat_message: { message: message },
        chat_history: { history: chat_history },
      }),
    });
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    await setAnswer("");
    reader.read().then(async function processStream({ done, value }) {
      if (done) {
        console.log("Stream complete");
        return;
      }

      // Value is a Uint8Array
      const dataStrings = decoder
        .decode(value)
        .split("data: ")
        .filter(Boolean);

      // You'll want to process this, parsing JSON strings as necessary and adding them to state

      dataStrings.forEach(async (data) => {
        try {
          const parsedData = JSON.parse(data);
          console.log(parsedData["token"]);
          await setAnswer((prevMessages) => prevMessages + parsedData["token"]);
          // sleep(1000)
        } catch (error) {
          console.error("Error parsing data:", error);
        }
      });
      // Read more stream data
      return reader.read().then(processStream);
    });
  } catch {
    await setAnswer("Network error occured");
  }
}

export async function leadCheck(thread_id, chatbot_id) {
  let data;
  data = await supabase
    .from("leads")
    .select("*")
    .eq("thread_id", thread_id)
    .eq("chatbot_id", chatbot_id);
  console.log("checkcheck", data);
  if (data.data.length > 0) {
    return true;
  } else {
    return false;
  }
}

export async function removeData(chat_id, thread_id) {
  let result;
  try {
    const response = await axios.post(leadURL, {
      action: "clear_chat_history",
      chatbot_id: chat_id,
      thread_id: thread_id,
    });
    result = response.data.success;
  } catch (error) {
    result = "fail";
  }
  console.log(result);
  return result;
}

export async function postLead(chat_id, thread_id, leadData) {
  let result;
  try {
    const response = await axios.post(leadURL, {
      action: "store_lead",
      chatbot_id: chat_id,
      thread_id: thread_id,
      lead: leadData,
    });
    result = response.data.success;
    console.log("eee", result);
  } catch (error) {
    result = "fail";
  }
  console.log(result);
  return result;
}

export async function getCountryCode() {
  const response = await axios.get("https://www.cloudflare.com/cdn-cgi/trace");
  let country_code = response.data.replace(/(\r\n|\n|\r)/gm, "").split("loc=");
  country_code = country_code[1].split("tls=");
  country_code = country_code[0];
  return country_code;
}
