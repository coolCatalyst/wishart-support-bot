import { supabaseUrl, supabaseKey, baseURL, leadURL } from "../../config";
import axios from "axios";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(supabaseUrl, supabaseKey);

export async function getData(ID) {
  let data;

  data = await supabase.from("chatbots").select("*").eq("id", ID);

  return data.data;
}

export async function postMessage(chat_id, thread_id, message, chat_history) {
  console.log('chathistory',chat_history);
  const result = await axios.post(baseURL, {
    "chat_message": {"message": message},
"chat_history": {"history": chat_history}
  });
  return result.data;
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
