package xyz.twinone.logsolve;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.flurgle.camerakit.CameraListener;
import com.flurgle.camerakit.CameraView;
import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.text.MessageFormat;

import cz.msebera.android.httpclient.Header;

public class MainActivity extends AppCompatActivity {


    private static final String FILENAME = "pic.jpg";
    private static final String SERVER = "http://192.168.1.101:5000";
    private static final String URL = SERVER + "/upload";


    private CameraView mCameraView;
    private ImageView mImageView;
    private Button mButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        mCameraView = (CameraView) findViewById(R.id.camera);
        mImageView = (ImageView) findViewById(R.id.image);
        mButton = (Button) findViewById(R.id.button);

        mButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("Main", "Click");
                takePicture();
            }
        });
        mImageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Log.d("Main", "Click");
                mCameraView.setVisibility(View.VISIBLE);
                mImageView.setVisibility(View.GONE);
            }
        });


        mCameraView.setCameraListener(new CameraListener() {
            @Override
            public void onPictureTaken(byte[] picture) {
                super.onPictureTaken(picture);

                // Create a bitmap
                Bitmap result = BitmapFactory.decodeByteArray(picture, 0, picture.length);
                try {
                    FileOutputStream os = openFileOutput(FILENAME, MODE_PRIVATE);
                    result.compress(Bitmap.CompressFormat.PNG, 100, os);
                    os.close();
                } catch (Exception e) {
                    Log.e("Main", "Error saving image: ", e);
                }


                try {
                    FileInputStream is = openFileInput(FILENAME);
                    RequestParams p = new RequestParams();
                    p.put("image.jpg", is);
                    AsyncHttpClient client = new AsyncHttpClient();
                    client.post(URL, p, new AsyncHttpResponseHandler() {
                        @Override
                        public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                            Log.d("Main", "Success");
                        }

                        @Override
                        public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
                            Log.d("Main", "Error, respcode="+statusCode, error);

                        }
                    });
                } catch (Exception e) {
                    Log.e("Main", "Error sending image: ", e);
                }

                mImageView.setImageBitmap(result);
                mImageView.setVisibility(View.VISIBLE);
                mCameraView.setVisibility(View.GONE);
            }
        });
    }

    private void takePicture() {
        mCameraView.captureImage();
    }

    @Override
    protected void onResume() {
        super.onResume();
        mCameraView.start();
    }

    @Override
    protected void onPause() {
        mCameraView.stop();
        super.onPause();
    }

}
