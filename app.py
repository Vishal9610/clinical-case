
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, db
from sqlalchemy import func, or_
from functools import wraps
from datetime import date
import uuid


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="DOCTOR")


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    sex = db.Column(db.String(20))
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(150))
    clinical_indication = db.Column(db.Text)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())


class Examination(db.Model):
    __tablename__ = "examinations"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer, db.ForeignKey("patients.id"), nullable=False
    )
    examination_type = db.Column(db.String(30), nullable=False)
    examination_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="DRAFT")
    clinical_observations = db.Column(db.Text)
    clinical_impression = db.Column(db.Text)
    created_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, server_default=func.now())
    patient = db.relationship("Patient", foreign_keys=[patient_id])


class XRayFinding(db.Model):
    __tablename__ = "xray_findings"

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(
        db.Integer,
        db.ForeignKey("examinations.id"),
        nullable=False,
        unique=True
    )

    # Existing fields retained for compatibility
    rotation = db.Column(db.String(30))
    inspiratory_film = db.Column(db.String(30))
    penetration = db.Column(db.String(30))
    situs = db.Column(db.String(30))
    cardiac_position = db.Column(db.String(30))
    cardiomegaly = db.Column(db.String(30))
    additional_notes = db.Column(db.Text)

    # Separate Chest X-Ray finding

    ra_enlargement = db.Column(db.String(50))
    la_enlargement = db.Column(db.String(50))
    rv_enlargement = db.Column(db.String(50))
    lv_enlargement = db.Column(db.String(50))

    thymic_shadow = db.Column(db.String(50))
    aorta_position_knuckle = db.Column(db.String(50))

    aa_dilatation = db.Column(db.String(50))
    da_dilatation = db.Column(db.String(50))
    mpa_dilatation = db.Column(db.String(50))
    rpa_dilatation = db.Column(db.String(50))
    lpa_dilatation = db.Column(db.String(50))

    pulmonary_plethora = db.Column(db.String(50))
    pulmonary_oligemia = db.Column(db.String(50))
    pah = db.Column(db.String(50))
    pvh = db.Column(db.String(50))


class ECGFinding(db.Model):
    __tablename__ = "ecg_findings"

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(
        db.Integer,
        db.ForeignKey("examinations.id"),
        nullable=False,
        unique=True
    )

    # Existing fields retained for compatibility
    sinus_rhythm = db.Column(db.String(30))
    heart_rate = db.Column(db.String(30))
    p_axis = db.Column(db.String(30))
    qrs_axis = db.Column(db.String(30))
    pr_interval = db.Column(db.String(30))
    qtc_interval = db.Column(db.String(30))
    qrs_duration = db.Column(db.String(30))
    bundle_branch_block = db.Column(db.String(50))
    st_segment = db.Column(db.String(50))
    additional_observations = db.Column(db.Text)

    # Separate ECG findings
    
    ra_enlargement_ecg = db.Column(db.String(50))
    la_enlargement_ecg = db.Column(db.String(50))
    rvh_pressure_overload = db.Column(db.String(50))
    rvh_volume_overload = db.Column(db.String(50))
    lvh_pressure_overload = db.Column(db.String(50))
    lvh_volume_overload = db.Column(db.String(50))
    bv_hypertrophy = db.Column(db.String(50))


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session.clear()
            session["user_id"] = user.id
            session["full_name"] = user.full_name
            session["role"] = user.role
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@app.route("/patients", methods=["GET"])
@login_required
def patients():
    search = request.args.get("search", "").strip()
    query = Patient.query

    if search:
        term = f"%{search}%"
        query = query.filter(
            db.or_(
                Patient.full_name.ilike(term),
                Patient.patient_id.ilike(term),
                Patient.mobile.ilike(term)
            )
        )

    patient_list = query.order_by(Patient.id.desc()).all()

    return render_template(
        "patients.html",
        patients=patient_list,
        search=search
    )


@app.route("/patients/new", methods=["GET", "POST"])
@login_required
def new_patient():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        dob_text = request.form.get("date_of_birth", "").strip()
        sex = request.form.get("sex", "").strip()
        mobile = request.form.get("mobile", "").strip()
        email = request.form.get("email", "").strip()
        indication = request.form.get("clinical_indication", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            flash("Patient name is required.", "error")
            return render_template("patient_form.html", patient=None)

        dob = None
        if dob_text:
            try:
                dob = date.fromisoformat(dob_text)
                if dob > date.today():
                    raise ValueError
            except ValueError:
                flash("Enter a valid date of birth.", "error")
                return render_template("patient_form.html", patient=None)

        patient = Patient(
            patient_id=f"TEMP-{uuid.uuid4().hex}",
            full_name=name,
            date_of_birth=dob,
            sex=sex or None,
            mobile=mobile or None,
            email=email or None,
            clinical_indication=indication or None,
            address=address or None
        )

        try:
            db.session.add(patient)
            db.session.flush()

            patient.patient_id = f"PT-{patient.id:04d}"
            db.session.commit()

            flash(
                f"Patient registered successfully: {patient.patient_id}",
                "success"
            )
            return redirect(url_for("patients"))

        except Exception:
            db.session.rollback()
            app.logger.exception("Patient registration failed")
            flash("Patient could not be saved. Please try again.", "error")

    return render_template("patient_form.html", patient=None)


@app.route("/patients/<int:patient_db_id>/edit", methods=["GET", "POST"])
@login_required
def edit_patient(patient_db_id):
    patient = db.get_or_404(Patient, patient_db_id)

    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        dob_text = request.form.get("date_of_birth", "").strip()

        if not name:
            flash("Patient name is required.", "error")
            return render_template("patient_form.html", patient=patient)

        try:
            dob = date.fromisoformat(dob_text) if dob_text else None
            if dob and dob > date.today():
                raise ValueError
        except ValueError:
            flash("Enter a valid date of birth.", "error")
            return render_template("patient_form.html", patient=patient)

        patient.full_name = name
        patient.date_of_birth = dob
        patient.sex = request.form.get("sex", "").strip() or None
        patient.mobile = request.form.get("mobile", "").strip() or None
        patient.email = request.form.get("email", "").strip() or None
        patient.clinical_indication = (
            request.form.get("clinical_indication", "").strip() or None
        )
        patient.address = request.form.get("address", "").strip() or None

        try:
            db.session.commit()
            flash("Patient details updated successfully.", "success")
            return redirect(url_for("patients"))
        except Exception:
            db.session.rollback()
            app.logger.exception("Patient update failed")
            flash("Patient could not be updated.", "error")

    return render_template("patient_form.html", patient=patient)



@app.route("/examinations/new", methods=["GET", "POST"])
@login_required
def new_examination():
    patient_list = Patient.query.order_by(Patient.full_name.asc()).all()

    def optional_text(field):
        return request.form.get(field, "").strip() or None

    if request.method == "POST":
        patient_id = request.form.get("patient_id", type=int)
        examination_type = request.form.get("examination_type", "").strip()
        examination_date_text = request.form.get("examination_date", "").strip()
        action = request.form.get("action", "draft")

        patient = db.session.get(Patient, patient_id) if patient_id else None

        if not patient:
            flash("Please select a valid patient.", "error")
        elif examination_type not in ("CHEST_XRAY", "ECG", "BOTH"):
            flash("Please select a valid examination type.", "error")
        else:
            try:
                if not examination_date_text:
                    raise ValueError("Examination date is required.")

                examination_date = date.fromisoformat(examination_date_text)

                if examination_date > date.today():
                    raise ValueError("Future date is not allowed.")

                examination = Examination(
                    patient_id=patient.id,
                    examination_type=examination_type,
                    examination_date=examination_date,
                    status="PENDING_REVIEW" if action == "review" else "DRAFT",
                    created_by=session["user_id"]
                )

                db.session.add(examination)
                db.session.flush()

                if examination_type in ("CHEST_XRAY", "BOTH"):
                    xray = XRayFinding(
                        examination_id=examination.id,
                        rotation=optional_text("rotation"),
                        inspiratory_film=optional_text("inspiratory_film"),
                        penetration=optional_text("penetration"),
                        situs=optional_text("situs"),
                        cardiac_position=optional_text("cardiac_position"),
                        cardiomegaly=optional_text("cardiomegaly"),
                        ra_enlargement=optional_text("ra_enlargement"),
                        la_enlargement=optional_text("la_enlargement"),
                        rv_enlargement=optional_text("rv_enlargement"),
                        lv_enlargement=optional_text("lv_enlargement"),
                        thymic_shadow=optional_text("thymic_shadow"),
                        aorta_position_knuckle=optional_text("aorta_position_knuckle"),
                        aa_dilatation=optional_text("aa_dilatation"),
                        da_dilatation=optional_text("da_dilatation"),
                        mpa_dilatation=optional_text("mpa_dilatation"),
                        rpa_dilatation=optional_text("rpa_dilatation"),
                        lpa_dilatation=optional_text("lpa_dilatation"),
                        pulmonary_plethora=optional_text("pulmonary_plethora"),
                        pulmonary_oligemia=optional_text("pulmonary_oligemia"),
                        pah=optional_text("pah"),
                        pvh=optional_text("pvh"),
                        additional_notes=optional_text("xray_notes")
                    )
                    db.session.add(xray)

                if examination_type in ("ECG", "BOTH"):
                    ecg = ECGFinding(
                        examination_id=examination.id,
                        sinus_rhythm=optional_text("sinus_rhythm"),
                        heart_rate=optional_text("heart_rate"),
                        p_axis=optional_text("p_axis"),
                        qrs_axis=optional_text("qrs_axis"),
                        pr_interval=optional_text("pr_interval"),
                        qtc_interval=optional_text("qtc_interval"),
                        qrs_duration=optional_text("qrs_duration"),
                        ra_enlargement_ecg=optional_text("ra_enlargement_ecg"),
                        la_enlargement_ecg=optional_text("la_enlargement_ecg"),
                        bundle_branch_block=optional_text("bundle_branch_block"),
                        rvh_pressure_overload=optional_text("rvh_pressure_overload"),
                        rvh_volume_overload=optional_text("rvh_volume_overload"),
                        lvh_pressure_overload=optional_text("lvh_pressure_overload"),
                        lvh_volume_overload=optional_text("lvh_volume_overload"),
                        bv_hypertrophy=optional_text("bv_hypertrophy"),
                        st_segment=optional_text("st_segment"),
                        additional_observations=optional_text("ecg_notes")
                    )
                    db.session.add(ecg)

                db.session.commit()
                flash("Examination saved successfully.", "success")
                return redirect(url_for("dashboard"))

            except (ValueError, TypeError):
                db.session.rollback()
                flash("Check the examination date and enter valid values.", "error")
            except Exception:
                db.session.rollback()
                app.logger.exception("Examination saving failed")
                flash("Examination could not be saved.", "error")

    return render_template(
        "examination_form.html",
        patients=patient_list,
        today=date.today().isoformat()
    )


@app.route("/examinations")
@login_required
def examinations():
    records = (
        db.session.query(Examination, Patient)
        .join(Patient, Examination.patient_id == Patient.id)
        .order_by(Examination.id.desc())
        .all()
    )

    return render_template("examinations.html", records=records)



@app.route("/examinations/<int:examination_id>")
@login_required
def examination_details(examination_id):
    examination = db.session.get(Examination, examination_id)

    if examination is None:
        abort(404)

    patient = db.session.get(Patient, examination.patient_id)

    xray = XRayFinding.query.filter_by(
        examination_id=examination.id
    ).first()

    ecg = ECGFinding.query.filter_by(
        examination_id=examination.id
    ).first()

    return render_template(
        "examination_details.html",
        examination=examination,
        patient=patient,
        xray=xray,
        ecg=ecg
    )


@app.route(
    "/examinations/<int:examination_id>/report",
    methods=["GET"]
)
@login_required
def examination_report(examination_id):
    examination = db.session.get(
        Examination,
        examination_id
    )

    if examination is None:
        abort(404)

    patient = db.session.get(
        Patient,
        examination.patient_id
    )

    if patient is None:
        abort(404)

    xray = XRayFinding.query.filter_by(
        examination_id=examination.id
    ).first()

    ecg = ECGFinding.query.filter_by(
        examination_id=examination.id
    ).first()

    return render_template(
        "examination_report.html",
        examination=examination,
        patient=patient,
        xray=xray,
        ecg=ecg
    )


@app.route("/reports")
@login_required
def reports():
    examinations = Examination.query.order_by(
        Examination.examination_date.desc()
    ).all()

    return render_template(
        "reports.html",
        examinations=examinations
    )




@app.route(
    "/examinations/<int:examination_id>/delete",
    methods=["POST"]
)
@login_required
def delete_examination(examination_id):
    examination = db.session.get(Examination, examination_id)

    if examination is None:
        flash("Examination not found.", "error")
        return redirect(url_for("examinations"))

    try:
        # Remove related X-Ray findings.
        XRayFinding.query.filter_by(
            examination_id=examination.id
        ).delete(synchronize_session=False)

        # Remove related ECG findings.
        ECGFinding.query.filter_by(
            examination_id=examination.id
        ).delete(synchronize_session=False)

        # Remove the examination record.
        db.session.delete(examination)
        db.session.commit()

        flash("Examination deleted successfully.", "success")

    except Exception:
        db.session.rollback()
        app.logger.exception("Examination deletion failed")
        flash("Examination could not be deleted.", "error")

    return redirect(url_for("examinations"))



@app.route("/examinations/<int:examination_id>/edit", methods=["GET", "POST"])
@login_required
def edit_examination(examination_id):
    examination = db.session.get(Examination, examination_id)

    if examination is None:
        abort(404)

    patient_list = Patient.query.order_by(
        Patient.full_name.asc()
    ).all()

    xray_sources = []
    ecg_sources = []

    def optional_text(field):
        return request.form.get(field, "").strip() or None

    if request.method == "POST":
        examination_type = request.form.get(
            "examination_type", ""
        ).strip()

        examination_date_text = request.form.get(
            "examination_date", ""
        ).strip()

        action = request.form.get("action", "draft")

        if examination_type not in ("CHEST_XRAY", "ECG", "BOTH"):
            flash("Please select a valid examination type.", "error")

        else:
            try:
                examination_date = date.fromisoformat(
                    examination_date_text
                )

                if examination_date > date.today():
                    raise ValueError("Future date is not allowed.")

                examination.examination_type = examination_type
                examination.examination_date = examination_date

                if action == "review":
                    examination.status = "PENDING_REVIEW"
                elif action == "draft":
                    examination.status = "DRAFT"

                # Update or create X-Ray findings when required.
                if examination_type in ("CHEST_XRAY", "BOTH"):
                    xray = XRayFinding.query.filter_by(
                        examination_id=examination.id
                    ).first()

                    if xray is None:
                        xray = XRayFinding(
                            examination_id=examination.id
                        )
                        db.session.add(xray)

                    for field in [
                        "rotation",
                        "inspiratory_film",
                        "penetration",
                        "situs",
                        "cardiac_position",
                        "cardiomegaly",
                        "ra_enlargement",
                        "la_enlargement",
                        "rv_enlargement",
                        "lv_enlargement",
                        "thymic_shadow",
                        "aorta_position_knuckle",
                        "aa_dilatation",
                        "da_dilatation",
                        "mpa_dilatation",
                        "rpa_dilatation",
                        "lpa_dilatation",
                        "pulmonary_plethora",
                        "pulmonary_oligemia",
                        "pah",
                        "pvh",
                    ]:
                        setattr(xray, field, optional_text(field))

                    xray.additional_notes = optional_text("xray_notes")

                # Update or create ECG findings when required.
                if examination_type in ("ECG", "BOTH"):
                    ecg = ECGFinding.query.filter_by(
                        examination_id=examination.id
                    ).first()

                    if ecg is None:
                        ecg = ECGFinding(
                            examination_id=examination.id
                        )
                        db.session.add(ecg)

                    for field in [
                        "sinus_rhythm",
                        "heart_rate",
                        "p_axis",
                        "qrs_axis",
                        "pr_interval",
                        "qtc_interval",
                        "qrs_duration",
                        "ra_enlargement_ecg",
                        "la_enlargement_ecg",
                        "bundle_branch_block",
                        "rvh_pressure_overload",
                        "rvh_volume_overload",
                        "lvh_pressure_overload",
                        "lvh_volume_overload",
                        "bv_hypertrophy",
                        "st_segment",
                    ]:
                        setattr(ecg, field, optional_text(field))

                    ecg.additional_observations = optional_text("ecg_notes")

                # Keep existing findings if the examination type changes.
                db.session.commit()

                flash("Examination updated successfully.", "success")

                return redirect(
                    url_for(
                        "examination_details",
                        examination_id=examination.id
                    )
                )

            except (ValueError, TypeError):
                db.session.rollback()
                flash("Check the examination date.", "error")

            except Exception:
                db.session.rollback()
                app.logger.exception("Examination update failed")
                flash("Examination could not be updated.", "error")

    # Load saved findings for the current examination.
    xray = XRayFinding.query.filter_by(
        examination_id=examination.id
    ).first()

    ecg = ECGFinding.query.filter_by(
        examination_id=examination.id
    ).first()

    # Find other examinations belonging to the same patient.
    other_examinations = Examination.query.filter(
        Examination.patient_id == examination.patient_id,
        Examination.id != examination.id
    ).order_by(
        Examination.examination_date.desc()
    ).all()

    for item in other_examinations:
        saved_xray = XRayFinding.query.filter_by(
            examination_id=item.id
        ).first()

        saved_ecg = ECGFinding.query.filter_by(
            examination_id=item.id
        ).first()

        if saved_xray is not None:
            xray_sources.append(item)

        if saved_ecg is not None:
            ecg_sources.append(item)

    return render_template(
        "examination_form.html",
        patients=patient_list,
        today=date.today().isoformat(),
        examination=examination,
        xray=xray,
        ecg=ecg,
        edit_mode=True,
        xray_sources=xray_sources,
        ecg_sources=ecg_sources
    )


@app.route(
    "/examinations/<int:examination_id>/load-findings/<kind>/<int:source_id>",
    methods=["GET"]
)
@login_required
def load_existing_findings(examination_id, kind, source_id):
    current = db.session.get(Examination, examination_id)
    source = db.session.get(Examination, source_id)

    if current is None or source is None:
        return jsonify({"error": "Examination not found."}), 404

    if current.patient_id != source.patient_id:
        return jsonify({
            "error": "Findings can only be loaded from the same patient."
        }), 403

    if current.id == source.id:
        return jsonify({
            "error": "Please select a different examination."
        }), 400

    if kind == "xray":
        record = XRayFinding.query.filter_by(
            examination_id=source.id
        ).first()

        fields = [
            "rotation", "inspiratory_film", "penetration",
            "situs", "cardiac_position", "cardiomegaly",
            "ra_enlargement", "la_enlargement",
            "rv_enlargement", "lv_enlargement",
            "thymic_shadow", "aorta_position_knuckle",
            "aa_dilatation", "da_dilatation",
            "mpa_dilatation", "rpa_dilatation",
            "lpa_dilatation", "pulmonary_plethora",
            "pulmonary_oligemia", "pah", "pvh"
        ]

        notes_field = "additional_notes"

    elif kind == "ecg":
        record = ECGFinding.query.filter_by(
            examination_id=source.id
        ).first()

        fields = [
            "sinus_rhythm", "heart_rate", "p_axis", "qrs_axis",
            "pr_interval", "qtc_interval", "qrs_duration",
            "ra_enlargement_ecg", "la_enlargement_ecg",
            "bundle_branch_block", "rvh_pressure_overload",
            "rvh_volume_overload", "lvh_pressure_overload",
            "lvh_volume_overload", "bv_hypertrophy", "st_segment"
        ]

        notes_field = "additional_observations"

    else:
        return jsonify({"error": "Invalid findings type."}), 400

    if record is None:
        return jsonify({
            "error": f"No saved {kind.upper()} findings in that examination."
        }), 404

    result = {
        field: getattr(record, field)
        for field in fields
    }

    result["xray_notes" if kind == "xray" else "ecg_notes"] = (
        getattr(record, notes_field) or ""
    )

    return jsonify(result)


@app.route("/dashboard")
@login_required
def dashboard():
    total_patients = Patient.query.count()
    total_examinations = Examination.query.count()

    total_xray = Examination.query.filter_by(
        examination_type="CHEST_XRAY"
    ).count()

    total_ecg = Examination.query.filter_by(
        examination_type="ECG"
    ).count()

    recent_examinations = (
        db.session.query(Examination, Patient)
        .join(Patient, Examination.patient_id == Patient.id)
        .order_by(Examination.id.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_patients=total_patients,
        total_examinations=total_examinations,
        total_xray=total_xray,
        total_ecg=total_ecg,
        recent_examinations=recent_examinations
    )




@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.cli.command("create-admin")
def create_admin():
    username = input("Admin username: ").strip()
    full_name = input("Admin full name: ").strip()
    password = input("Admin password: ")

    if not username or not full_name or not password:
        print("All fields are required.")
        return

    if User.query.filter_by(username=username).first():
        print("Username already exists.")
        return

    user = User(
        username=username,
        full_name=full_name,
        password_hash=generate_password_hash(password),
        role="SUPER_ADMIN"
    )

    db.session.add(user)
    db.session.commit()

    print("Admin account created successfully.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
