import java.sql.*;
//import oracle.jdbc;

public class DatabaseConnection {

    private Connection myConn;
    private Statement myStatement;
    private ResultSet myResults;
    private ResultSetMetaData myResultMetaData;
    private String url = "jdbc:oracle:thin:collingee/46LS3U1A3e8ZnSko0eDeR3up@oracle.cise.ufl.edu:1521:orcl";
    private String testQuery = "SELECT * FROM CLASS";
    private String myQuery;
    private PreparedStatement myPreparedStatement;

    public void getConnection() {
        try {
            this.myConn = DriverManager.getConnection(this.url);
            this.myConn.setAutoCommit(true);
            this.myStatement = this.myConn.createStatement();
        } catch (Exception e) {
            System.out.println("In the error block...why?");
            e.printStackTrace();
        }
    }

    public ResultSet getResultSet(String query) {
        try {
            this.myResults = myStatement.executeQuery(query);
            this.myResultMetaData = this.myResults.getMetaData();
            // this.myHeaders = myResultMetaData.getColumnLabel(1);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return this.myResults;
    }

    public void printResultSet() {
        try {

            // Print out the query value
            System.out.println();
            System.out.println("Query: " + this.myQuery);

            // Print out the headers
            System.out.println();
            for (int i = 1; i <= myResultMetaData.getColumnCount(); i++) {
                System.out.print(myResultMetaData.getColumnLabel(i) + "\t");
            }
            System.out.println();
            while (this.myResults.next()) {
                System.out.println(this.myResults.getString(1) + "\t" + this.myResults.getString(2) + "\t\t"
                        + this.myResults.getString(3));
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void closeConnection() {
        try {
            myConn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void getClassValues() {
        this.myQuery = "SELECT * FROM CLASS";
        getResultSet(myQuery);
        printResultSet();
    }

    public void getUsersValues() {
        this.myQuery = "SELECT * FROM USERS";
        getResultSet(myQuery);
        printResultSet();
    }

    public void getVideoValues() {
        this.myQuery = "SELECT * FROM VIDEO";
        getResultSet(myQuery);
        printResultSet();
    }

    public static void main(String args[]) {
        DatabaseConnection db = new DatabaseConnection();
        db.getConnection();
        db.getClassValues();
        db.getUsersValues();
        db.getVideoValues();
        db.closeConnection();
    }

    // WILL NEED TO DO .COMMIT WHEN PUSHING DATA IN/DELETING DATA FROM DATABASE
}