#include <iostream>
#include <vector>
#include <string>

using namespace std;

// Struct to store voucher information
struct Voucher {
    int id;
    string code;
    string category;
    string description;
    bool isClaimed;

    Voucher(int i, string c, string cat, string desc, bool claimed)
        : id(i), code(c), category(cat), description(desc), isClaimed(claimed) {}
};

// Function prototypes
void displayMenu();
void displayAllVouchers(const vector<Voucher>& vouchers);
void displayVouchersByCategory(const vector<Voucher>& vouchers, const string& category);
void claimVoucher(vector<Voucher>& vouchers);

int main() {
    vector<Voucher> vouchers;
    vouchers.push_back(Voucher(1, "FS-100", "Free Shipping", "Free Shipping Min Spend RM15", false));
    vouchers.push_back(Voucher(2, "FOOD-20", "Food & Beverage", "20% OFF Food Delivery", false));
    vouchers.push_back(Voucher(3, "ELEC-50", "Electronics", "RM50 OFF Minimum Spend RM500", false));
    vouchers.push_back(Voucher(4, "FASH-15", "Fashion", "15% OFF Apparel", false));
    vouchers.push_back(Voucher(5, "FS-200", "Free Shipping", "Free Shipping Min Spend RM0", false));

    int choice = 0;
    do {
        displayMenu();
        cout << "Enter choice (1-4): ";
        cin >> choice;

        if (cin.fail()) {
            cin.clear();
            cin.ignore(10000, '\n');
            cout << "Invalid selection! Please enter a number between 1 and 4.\n";
            continue;
        }

        switch (choice) {
            case 1:
                displayAllVouchers(vouchers);
                break;
            case 2: {
                cout << "\nSelect Category Navigation:\n";
                cout << "1. Free Shipping\n2. Food & Beverage\n3. Electronics\n4. Fashion\nChoice: ";
                int catChoice;
                cin >> catChoice;
                if (cin.fail()) {
                    cin.clear();
                    cin.ignore(10000, '\n');
                    cout << "Invalid choice!\n";
                    break;
                }
                if (catChoice == 1) displayVouchersByCategory(vouchers, "Free Shipping");
                else if (catChoice == 2) displayVouchersByCategory(vouchers, "Food & Beverage");
                else if (catChoice == 3) displayVouchersByCategory(vouchers, "Electronics");
                else if (catChoice == 4) displayVouchersByCategory(vouchers, "Fashion");
                else cout << "Invalid category selection.\n";
                break;
            }
            case 3:
                claimVoucher(vouchers);
                break;
            case 4:
                cout << "Exiting Shopee Voucher System. Thank you!\n";
                break;
            default:
                cout << "Invalid menu selection. Try again.\n";
        }
    } while (choice != 4);

    return 0;
}

void displayMenu() {
    cout << "\n=========================================\n";
    cout << "   SHOPEE VOUCHER NAVIGATION SYSTEM      \n";
    cout << "=========================================\n";
    cout << "1. View All Vouchers\n";
    cout << "2. Navigate / Filter by Category\n";
    cout << "3. Claim Voucher\n";
    cout << "4. Exit\n";
    cout << "=========================================\n";
}

void displayAllVouchers(const vector<Voucher>& vouchers) {
    cout << "\n--- All Available Vouchers ---\n";
    for (size_t i = 0; i < vouchers.size(); ++i) {
        string status = vouchers[i].isClaimed ? "CLAIMED" : "AVAILABLE";
        cout << "[" << vouchers[i].id << "] " << vouchers[i].code << " | Category: " << vouchers[i].category
             << " | " << vouchers[i].description << " | Status: " << status << "\n";
    }
}

void displayVouchersByCategory(const vector<Voucher>& vouchers, const string& category) {
    cout << "\n--- Category: " << category << " ---\n";
    bool found = false;
    for (size_t i = 0; i < vouchers.size(); ++i) {
        if (vouchers[i].category == category) {
            string status = vouchers[i].isClaimed ? "CLAIMED" : "AVAILABLE";
            cout << "[" << vouchers[i].id << "] " << vouchers[i].code << " | " << vouchers[i].description
                 << " | Status: " << status << "\n";
            found = true;
        }
    }
    if (!found) cout << "No vouchers found in this category.\n";
}

void claimVoucher(vector<Voucher>& vouchers) {

    cout << "\n--- Available Vouchers to Claim ---\n";
    bool found = false;

    for (size_t i = 0; i < vouchers.size(); ++i) {
    if (!vouchers[i].isClaimed) {
            cout << "[" << vouchers[i].id << "] "
                << vouchers[i].code
                << " | Category: " << vouchers[i].category
                << " | " << vouchers[i].description
                << "\n";

            found = true;
        }
    }

    if (!found) {
    cout << "No available vouchers to claim.\n";
    return;
    }

    int id;
    cout << "\nEnter Voucher ID to claim: ";
    cin >> id;

    if (cin.fail()) {
        cin.clear();
        cin.ignore(10000, '\n');
        cout << "Invalid input! Please enter a valid numeric Voucher ID.\n";
        return;
    }

    for (size_t i = 0; i < vouchers.size(); ++i) {
        if (vouchers[i].id == id) {
            if (vouchers[i].isClaimed) {
                cout << "Voucher has already been claimed!\n";
            } else {
                vouchers[i].isClaimed = true;
                cout << "Success! Claimed voucher: " << vouchers[i].code << "\n";
            }
            return;
        }
    }
    cout << "Voucher ID not found.\n";
}