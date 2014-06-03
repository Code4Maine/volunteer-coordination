package com.example.VolunteerHubApp;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.support.v4.view.ViewPager;
import android.support.v7.app.ActionBarActivity;
import android.util.Log;
import android.view.*;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.CookieStore;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.protocol.ClientContext;
import org.apache.http.impl.client.BasicCookieStore;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.cookie.BasicClientCookie;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

public class MainActivity extends ActionBarActivity {
    private static TextView tv;
    private static Button loginButton;

    private static ViewPager mViewPager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Create the adapter that will return a fragment for each of the three
        // primary sections of the activity.
        /*
      The {@link android.support.v4.view.PagerAdapter} that will provide
      fragments for each of the sections. We use a {@link FragmentPagerAdapter}
      derivative, which will keep every loaded fragment in memory. If this
      becomes too memory intensive, it may be best to switch to a
      {@link android.support.v4.app.FragmentStatePagerAdapter}.
     */
        SectionsPagerAdapter mSectionsPagerAdapter = new SectionsPagerAdapter(getSupportFragmentManager());


        // Set up the ViewPager with the sections adapter.
        /*
      The {@link ViewPager} that will host the section contents.
     */
        mViewPager = (ViewPager) findViewById(R.id.pager);
        mViewPager.setAdapter(mSectionsPagerAdapter);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {

        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        return id == R.id.action_settings || super.onOptionsItemSelected(item);
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment {
        /**
         * The fragment argument representing the section number for this
         * fragment.
         */
        private static final String ARG_SECTION_NUMBER = "section_number";

        public PlaceholderFragment() {
        }

        /**
         * Returns a new instance of this fragment for the given section number.
         */
        public static PlaceholderFragment newInstance(int sectionNumber) {
            PlaceholderFragment fragment = new PlaceholderFragment();
            Bundle args = new Bundle();
            args.putInt(ARG_SECTION_NUMBER, sectionNumber);
            fragment.setArguments(args);
            return fragment;
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
            ViewGroup rootView = null;
            if (getArguments().getInt(ARG_SECTION_NUMBER) == 1) {
                rootView = (ViewGroup) inflater.inflate(R.layout.home, container, false);
                Button login_button = (Button) rootView.findViewById(R.id.login_button);
                login_button.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        mViewPager.setCurrentItem(1);
                    }
                });
                Button create_account = (Button) rootView.findViewById(R.id.create_account);
                create_account.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        mViewPager.setCurrentItem(2);
                    }
                });
                Button volunteer_projects = (Button) rootView.findViewById(R.id.volunteer_projects);
                volunteer_projects.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        mViewPager.setCurrentItem(0);
                    }
                });
                Thread t = new Thread(new GetOpportunities());
                t.start();
            } else if (getArguments().getInt(ARG_SECTION_NUMBER) == 2) {
                rootView = (ViewGroup) inflater.inflate(R.layout.login, container, false);
                loginButton = (Button) rootView.findViewById(R.id.login_submit);
                final ViewGroup finalRootView = rootView;
                loginButton.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        EditText user_email_input = (EditText) finalRootView.findViewById(R.id.textEmailAddress);
                        String user_email = user_email_input.getText().toString();
                        EditText user_password_input = (EditText) finalRootView.findViewById(R.id.textPassword);
                        String user_password = user_password_input.getText().toString();
                        Thread t = new Thread(new UserLogin(getActivity().getApplicationContext(), user_email, user_password));
                        t.start();
                    }
                });
            } else {
                rootView = (ViewGroup) inflater.inflate(R.layout.fragment_main, container, false);
            }
            return rootView;
        }

        // /<slug>/opportunities/<slug>.json
        class GetOpportunities implements Runnable {

            // Define the Handler that receives messages from the thread and update the progress
            private final Handler handler = new Handler() {
                public void handleMessage(Message msg) {
                    String aResponse = msg.getData().getString("message");
                    tv.setText(aResponse);
                }
            };

            @Override
            public void run() {
                String description_parsed;
                StringBuilder builder = new StringBuilder();
                HttpClient client = new DefaultHttpClient();
                HttpGet httpGet = new HttpGet(
                        "http://162.243.174.10/14-elm-street/opportunities/json");
                try {
                    HttpResponse response = client.execute(httpGet);
                    HttpEntity entity = response.getEntity();
                    InputStream content = entity.getContent();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(content));
                    try {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            builder.append(line);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    } finally {
                        try {
                            if (reader != null) {
                                reader.close();
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    try {
                        JSONObject temp = new JSONObject(builder.toString());
                        description_parsed = temp.getString("description");
                        threadMsg(description_parsed);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    System.out.println("Exception Stuff");
                }
            }

            private void threadMsg(String msg) {

                if (!msg.equals(null) && !msg.equals("")) {
                    Message msgObj = handler.obtainMessage();
                    Bundle b = new Bundle();
                    b.putString("message", msg);
                    msgObj.setData(b);
                    handler.sendMessage(msgObj);
                }
            }
        }

        // /accounts/login
        class UserLogin implements Runnable {
            private Context context;
            private String email_address;
            private String password;

            public UserLogin(Context context, String email_address, String password) {
                this.context = context;
                this.email_address = email_address;
                this.password = password;
            }

            // Define the Handler that receives messages from the thread and update the progress
            private final Handler handler = new Handler() {
                public void handleMessage(Message msg) {
                    String aResponse = msg.getData().getString("message");
                    Toast.makeText(context, aResponse, Toast.LENGTH_SHORT).show();
                }
            };
            private final Handler buttonHandler = new Handler() {
                public void handleMessage(Message msg) {
                    String aResponse = msg.getData().getString("message");
                    if(loginButton == null)
                        return;
                    if(aResponse == "lock"){
                        loginButton.setEnabled(false);
                        loginButton.setText("Logging In");
                    } else {
                        loginButton.setEnabled(true);
                        loginButton.setText("Login");
                    }
                }
            };

            @Override
            public void run() {
                LockButton();
                String token = GetCSRFToken();

                HttpClient client = new DefaultHttpClient();
                HttpContext localContext = new BasicHttpContext();

                // HTTP parameters stores header etc.
                HttpParams params = new BasicHttpParams();
                params.setParameter("http.protocol.handle-redirects", false);

                // Create a local instance of cookie store
                CookieStore cookieStore = new BasicCookieStore();
                BasicClientCookie token_cookie = new BasicClientCookie("csrftoken", token);
                token_cookie.setDomain("162.243.174.10");
                token_cookie.setPath("/");
                cookieStore.addCookie(token_cookie);

                // Bind custom cookie store to the local context
                localContext.setAttribute(ClientContext.COOKIE_STORE, cookieStore);

                // connect and receive
                HttpPost httpPost = new HttpPost("http://162.243.174.10/accounts/login/");
                httpPost.setParams(params);


                try {
                    // Add your data
                    List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);

                    this.email_address = "poo@poo.com";
                    this.password = "test123";

                    nameValuePairs.add(new BasicNameValuePair("login", this.email_address));
                    nameValuePairs.add(new BasicNameValuePair("password", this.password));
                    nameValuePairs.add(new BasicNameValuePair("csrfmiddlewaretoken", token));
                    httpPost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

                    HttpResponse response = client.execute(httpPost,localContext);

                    //If it redirected us, we are ok, it logged us in.
                    int statusCode = response.getStatusLine().getStatusCode();
                    if (statusCode == 302) {
                        Intent intent = new Intent(context, LoggedInActivity.class);
                        startActivity(intent);
                    } else if(statusCode == 200) {
                        AlertUser("Invalid Username or Password");
                    } else {
                        AlertUser("An error occurred, the error code was: " + statusCode);
                    }
                } catch (Exception e) {
                    System.out.println("Exception Stuff");
                }
                UnlockButton();
            }
            private String GetCSRFToken(){
                try {
                    Document doc = Jsoup.connect("http://162.243.174.10/accounts/login/").get();
                    Elements csrf = doc.select("input[name=csrfmiddlewaretoken]");
                    return csrf.val();
                } catch (IOException e) {
                    e.printStackTrace();
                }

                return "";
            }
            private void LockButton() {
                Message msgObj = buttonHandler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("message", "lock");
                msgObj.setData(b);
                buttonHandler.sendMessage(msgObj);
            }
            private void UnlockButton() {
                Message msgObj = buttonHandler.obtainMessage();
                Bundle b = new Bundle();
                b.putString("message", "");
                msgObj.setData(b);
                buttonHandler.sendMessage(msgObj);
            }
            private void AlertUser(String msg) {
                if (!msg.equals(null) && !msg.equals("")) {
                    Message msgObj = handler.obtainMessage();
                    Bundle b = new Bundle();
                    b.putString("message", msg);
                    msgObj.setData(b);
                    handler.sendMessage(msgObj);
                }
            }
        }

        // /accounts/signup
        class UserCreateAccount implements Runnable {

            // Define the Handler that receives messages from the thread and update the progress
            private final Handler handler = new Handler() {
                public void handleMessage(Message msg) {
                    String aResponse = msg.getData().getString("message");
                    tv.setText(aResponse);
                }
            };

            @Override
            public void run() {
                String description_parsed;
                StringBuilder builder = new StringBuilder();
                HttpClient client = new DefaultHttpClient();
                HttpGet httpGet = new HttpGet(
                        "http://162.243.174.10/14-elm-street/opportunities/json");
                try {
                    HttpResponse response = client.execute(httpGet);
                    HttpEntity entity = response.getEntity();
                    InputStream content = entity.getContent();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(content));
                    try {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            builder.append(line);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    } finally {
                        try {
                            if (reader != null) {
                                reader.close();
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    try {
                        JSONObject temp = new JSONObject(builder.toString());
                        description_parsed = temp.getString("description");
                        threadMsg(description_parsed);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    System.out.println("Exception Stuff");
                }
            }

            private void threadMsg(String msg) {

                if (!msg.equals(null) && !msg.equals("")) {
                    Message msgObj = handler.obtainMessage();
                    Bundle b = new Bundle();
                    b.putString("message", msg);
                    msgObj.setData(b);
                    handler.sendMessage(msgObj);
                }
            }
        }

        // /projects/<slug>.json
        class getProjects implements Runnable {

            // Define the Handler that receives messages from the thread and update the progress
            private final Handler handler = new Handler() {
                public void handleMessage(Message msg) {
                    String aResponse = msg.getData().getString("message");
                    tv.setText(aResponse);
                }
            };

            @Override
            public void run() {
                String description_parsed;
                StringBuilder builder = new StringBuilder();
                HttpClient client = new DefaultHttpClient();
                HttpGet httpGet = new HttpGet(
                        "http://162.243.174.10/14-elm-street/opportunities/json");
                try {
                    HttpResponse response = client.execute(httpGet);
                    HttpEntity entity = response.getEntity();
                    InputStream content = entity.getContent();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(content));
                    try {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            builder.append(line);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    } finally {
                        try {
                            if (reader != null) {
                                reader.close();
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    try {
                        JSONObject temp = new JSONObject(builder.toString());
                        description_parsed = temp.getString("description");
                        threadMsg(description_parsed);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    System.out.println("Exception Stuff");
                }
            }

            private void threadMsg(String msg) {

                if (!msg.equals(null) && !msg.equals("")) {
                    Message msgObj = handler.obtainMessage();
                    Bundle b = new Bundle();
                    b.putString("message", msg);
                    msgObj.setData(b);
                    handler.sendMessage(msgObj);
                }
            }
        }

        // /organizations/<slug>.json
        class getOrganizations implements Runnable {

            // Define the Handler that receives messages from the thread and update the progress
            private final Handler handler = new Handler() {
                public void handleMessage(Message msg) {
                    String aResponse = msg.getData().getString("message");
                    tv.setText(aResponse);
                }
            };

            @Override
            public void run() {
                String description_parsed;
                StringBuilder builder = new StringBuilder();
                HttpClient client = new DefaultHttpClient();
                HttpGet httpGet = new HttpGet(
                        "http://162.243.174.10/14-elm-street/opportunities/json");
                try {
                    HttpResponse response = client.execute(httpGet);
                    HttpEntity entity = response.getEntity();
                    InputStream content = entity.getContent();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(content));
                    try {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            builder.append(line);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    } finally {
                        try {
                            if (reader != null) {
                                reader.close();
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                    try {
                        JSONObject temp = new JSONObject(builder.toString());
                        description_parsed = temp.getString("description");
                        threadMsg(description_parsed);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                } catch (Exception e) {
                    System.out.println("Exception Stuff");
                }
            }

            private void threadMsg(String msg) {

                if (!msg.equals(null) && !msg.equals("")) {
                    Message msgObj = handler.obtainMessage();
                    Bundle b = new Bundle();
                    b.putString("message", msg);
                    msgObj.setData(b);
                    handler.sendMessage(msgObj);
                }
            }
        }
    }

    /**
     * A {@link FragmentPagerAdapter} that returns a fragment corresponding to
     * one of the sections/tabs/pages.
     */
    public class SectionsPagerAdapter extends FragmentPagerAdapter {

        public SectionsPagerAdapter(FragmentManager fm) {
            super(fm);
        }

        @Override
        public Fragment getItem(int position) {
            // getItem is called to instantiate the fragment for the given page.
            // Return a PlaceholderFragment (defined as a static inner class
            // below).
            return PlaceholderFragment.newInstance(position + 1);
        }

        @Override
        public int getCount() {
            // Show 3 total pages.
            return 3;
        }

        @Override
        public CharSequence getPageTitle(int position) {
            Locale l = Locale.getDefault();
            switch (position) {
                case 0:
                    return getString(R.string.title_section1).toUpperCase(l);
                case 1:
                    return getString(R.string.title_section2).toUpperCase(l);
                case 2:
                    return getString(R.string.title_section3).toUpperCase(l);
            }
            return null;
        }
    }

    public void showToast(final String toast) {
        runOnUiThread(new Runnable() {
            public void run() {
                Toast.makeText(MainActivity.this, toast, Toast.LENGTH_SHORT).show();
            }
        });
    }
}
