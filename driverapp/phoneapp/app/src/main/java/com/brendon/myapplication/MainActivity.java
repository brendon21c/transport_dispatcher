package com.brendon.myapplication;

import android.nfc.Tag;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {


    Button mDriverIdButton;
    TextView mDriverDisplay;
    EditText mDriverEntryField;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mDriverIdButton = (Button) findViewById(R.id.mDriverIdButton);
        mDriverDisplay = (TextView) findViewById(R.id.mDriverDisplay);
        mDriverEntryField = (EditText) findViewById(R.id.mDriverEntryField);


        mDriverIdButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                int driverId = Integer.parseInt(mDriverEntryField.getText().toString());

                if (mDriverEntryField == null) {

                    Toast.makeText(getApplicationContext(), "empty field", Toast.LENGTH_LONG);
                } else {

                    try {

                        String url_string = "http://10.0.2.2:5000/api/routes/?driverid=" + driverId;

                        new getDriverRoute().execute(url_string);



                    } catch (Exception e) {

                        e.printStackTrace();
                        System.out.println("error: " + e);
                    }
                }


            }
        });


    }


    private class getDriverRoute extends AsyncTask<String, Void, JSONObject> {

        @Override
        protected JSONObject doInBackground(String... urls) {

            try {

                URL url = new URL(urls[0]);

                HttpURLConnection connection = (HttpURLConnection) url.openConnection();

                InputStream responseStream = connection.getInputStream();

                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(responseStream));

                StringBuilder stringBuilder = new StringBuilder();

                String line;

                while ((line = bufferedReader.readLine()) != null) {

                    stringBuilder.append(line);

                }

                String responseString = stringBuilder.toString();

                System.out.println(responseString);




            } catch (Exception e) {

                Log.e("error", "Error connecting to API", e);
                e.printStackTrace();
                System.out.println("error: " + e);

            }

            
            return null;


        }
    }


}
