import { supabaseUrl, supabaseKey, leadURL } from "../../config";
import axios from "axios";
import { createClient } from "@supabase/supabase-js";
import { config } from "../../config/config";
const baseURL = process.env.NEXT_PUBLIC_API_URL;

const supabase = createClient(supabaseUrl, supabaseKey);
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
export async function getData(ID) {
  return config;
}

async function concatenateStringToColumn(chatID, appendString) {
  try {
    // Fetch the original data
    let { data, error } = await supabase
      .from('Messages')
      .select("Content")
      .eq('ChatID', chatID)
    // .single();
    console.log('data: ', data, '\n Error: ', error)

    if (error) {
      console.log('here')
      // data = ""
    };


    // Check if the column data exists
    if (data.length > 0) {
      console.log('1111111111111111111', data[0]['Content'])
      // Concatenate new string with existing data

      const updatedValue = data[0]['Content'] + appendString;
      console.log('updatedValue: ',)

      // Update the data with the concatenated string
      const { data: updatedData, error: updateError } = await supabase
        .from('Messages')
        .update({ 'Content': updatedValue })
        .eq('ChatID', chatID);
      if (updateError) throw updateError;
      // Successfully updated the record
      console.log('Successfully updated record:', updatedData);
    } else {
      const { data, error } = await supabase
        .from('Messages')
        .insert({ 'ChatID': chatID, 'Content': appendString })
      console.log('here', data)
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

export async function postMessage(message, chat_history, setAnswer, chatID) {
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
        chat_history: { history: [] },
      }),
    });
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    await setAnswer("");
    let finalData = ""
    reader.read().then(async function processStream({ done, value }) {

      if (done) {
        console.log("Stream complete");
        await concatenateStringToColumn(chatID,  ",["+message+","+finalData+"]")
        // await insertData(chatID, [message, finalData].toString());
        console.log('here', await reader.read())
        return;
      }
      const dataStrings = decoder
        .decode(value)
        .split("data: ")
        .filter(Boolean);
      // Value is a Uint8Array
      // You'll want to process this, parsing JSON strings as necessary and adding them to state

      dataStrings.forEach(async (data) => {
        try {
          const parsedData = JSON.parse(data);
          console.log(parsedData["token"]);
          await setAnswer((prevMessages) => prevMessages + parsedData["token"]);
          finalData = finalData + parsedData["token"];
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

export async function leadCheck(chatID) {
  let data;
  data = await supabase
    .from("Leads")
    .select("*")
    .eq("ChatID", chatID)
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

export async function postLead(chat_id, leadData) {
  let result;
  const { data, error } = await supabase
    .from('Leads')
    .insert([
      { 'ChatID': chat_id, 'Lead': leadData } // Replace with actual column names and values
    ]);

  if (error) {
    console.error('Error inserting data:', error);
    return null;
  }

  console.log('Inserted data:', data);
  return true;
}

export async function getCountryCode() {
  const response = await axios.get("https://www.cloudflare.com/cdn-cgi/trace");
  let country_code = response.data.replace(/(\r\n|\n|\r)/gm, "").split("loc=");
  country_code = country_code[1].split("tls=");
  country_code = country_code[0];
  return country_code;
}
