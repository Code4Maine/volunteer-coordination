package com.example.volunteerhubapp;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONObject;

import android.view.ViewGroup;
import android.widget.TextView;

public class NetworkOperations implements Runnable {

	@Override
	public void run() {
		/*rootView = (ViewGroup) inflater.inflate(R.layout.home,
				container, false);
		StringBuilder builder = new StringBuilder();
		HttpClient client = new DefaultHttpClient();
		HttpGet httpGet = new HttpGet(
				"http://volunteerhub.me/14-elm-street/opportunities/json");
		try {
			HttpResponse response = client.execute(httpGet);
			HttpEntity entity = response.getEntity();
			InputStream content = entity.getContent();
			BufferedReader reader = new BufferedReader(
					new InputStreamReader(content));
			String line = "";
			while ((line = reader.readLine()) != null) {
				builder.append(line);
			}
			JSONObject temp = new JSONObject(builder.toString());
			description_parsed = temp.getString("description");
		} catch (Exception e) {
			System.out.println("Exception Stuff");
		}

		TextView textview = new TextView(rootView.getContext());
		textview.setText(description_parsed);
		rootView.addView(textview);*/

	}

}
